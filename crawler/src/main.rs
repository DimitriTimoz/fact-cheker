use std::hash::{DefaultHasher, Hash, Hasher};
use std::sync::Arc;
use std::time::{Duration, Instant};
use futures::stream::FuturesUnordered;
use futures::StreamExt;
use newspaper::{Newspaper, NewspaperModel, Paper};
use scraper::Selector;
use spider::page::Page;
use spider::tokio;
use spider::website::Website;

use meilisearch_sdk::client::*;
use tokio::sync::mpsc::error::SendError;
use tokio::sync::{mpsc, Semaphore};

pub mod newspaper;


fn hash_to_string(hash: u64) -> String {
    format!("{:x}", hash)  
}

async fn indexing(papers: &[Paper]) {
    if papers.is_empty() {
        println!("No papers to index");
        return;
    }

    println!("Indexing {} papers", papers.len());
    let client = Client::new(
         std::env::var("MEILISEARCH_URL").unwrap_or("http://localhost:7700".to_string()),
        Some("a"),
    )
    .unwrap();

    match client
        .index("papers")
        .add_documents(papers, Some("hash_url"))
        .await
    {
        Ok(_) => println!("Indexing done"),
        Err(e) => println!("Error: {}", e),
    }
}

async fn process_page(page: Page, paper: &Newspaper) -> Option<Paper> {

    let html = page.get_html();
    if page.is_empty() {
        return None;
    }
    let mut hasher: DefaultHasher = DefaultHasher::new();

    let document = scraper::Html::parse_document(&html);
    let mut title = page.get_url().to_string();
    for selector in paper.get_selectors() {
        let texts = document
            .select(selector)
            .filter(|element| {
                let name = element.value().name();
                // TODO: check this works
                name != "style" && name != "script" && name != "img"
            })
            .flat_map(|el| el.text())
            .collect::<Vec<_>>();
        if texts.is_empty() {
            continue;
        }

        for title_selector in ["h1", "h2", "h3", "h4", "h5", "h6"].iter() {
            if let Some(t) = document
                .select(&Selector::parse(title_selector).unwrap())
                .next()
            {
                title = t.text().collect::<Vec<_>>().join(" ");
                break;
            }
        }

        page.get_url().hash(&mut hasher);
        return Some(Paper {
            title,
            url: page.get_url().to_string(),
            content: texts.join(" "),
            hash_url: hash_to_string(hasher.finish()),
        });
    }
    None
}

const MAX_CONCURRENT_PROCESSING: usize = 10;
const QUEUE_SIZE: usize = 1000;

async fn scrape_website(paper: Newspaper, website: &mut Website) {
    let (tx, mut rx) = mpsc::channel(QUEUE_SIZE);
    let semaphore = Arc::new(Semaphore::new(MAX_CONCURRENT_PROCESSING));
    let mut rx2 = website.subscribe(QUEUE_SIZE).unwrap();

    // Tâche de réception
    let receive_task = tokio::spawn(async move {
        loop {
            match rx2.recv().await {
                Ok(page) => {
                    match tx.send(page).await {
                        Ok(_) => {}
                        Err(e) => {
                            println!("Channel error: {}", e);
                            break;
                        }
                        
                    }
                }
                Err(e) => {
                    println!("Error: {}", e);
                    break;
                }
            }
        }
    });

    // Tâche de traitement
    let process_task = tokio::spawn(async move {
        let mut futures = FuturesUnordered::new();
        let mut papers = Vec::new();
        let mut fetched = 0;

        loop {
            tokio::select! {
                Some(page) = rx.recv() => {
                    let sem_clone = semaphore.clone();
                    let paper_clone = paper.clone();
                    futures.push(async move {
                        let _permit = sem_clone.acquire().await.unwrap();
                        process_page(page, &paper_clone).await
                    });
                }
                Some(processed_paper) = futures.next() => {
                    if let Some(paper) = processed_paper {
                        papers.push(paper);
                        if papers.len() >= 80 {
                            indexing(papers.as_slice()).await;
                            fetched += papers.len();
                            papers.clear();
                        }
                    }
                }
                else => break,
            }
        }

        if !papers.is_empty() {
            indexing(papers.as_slice()).await;
            fetched += papers.len();
        }
        println!("Fetched total of {} papers", fetched);
    });

    website.crawl().await;
    website.unsubscribe();

    receive_task.await.unwrap();
    process_task.await.unwrap();
}


#[tokio::main]
async fn main() {
    let file = std::fs::File::open("newspapers.json").unwrap();
    let newspapers: Vec<NewspaperModel> = serde_json::from_reader(file).unwrap();

    let mut i = 0;
    loop {
        i += 1;
        let newspapers = newspapers
            .iter()
            .map(|newspaper| Newspaper::from(newspaper.clone()));

        for paper in newspapers {
            let mut website = Website::new(paper.get_url());
            website.with_limit((10_000 * i).min(100_000));
            println!("Scraping {}", paper.get_title());
            scrape_website(paper, &mut website).await;
        }
        tokio::time::sleep(std::time::Duration::from_secs(60*60)).await;
    }
}
