use std::hash::{DefaultHasher, Hash, Hasher};
use newspaper::{Newspaper, NewspaperModel, Paper};
use scraper::Selector;
use spider::page::Page;
use spider::tokio;
use spider::website::Website;

use meilisearch_sdk::client::*;

pub mod newspaper;

async fn indexing(papers: &[Paper]) {
    if papers.is_empty() {
        println!("No papers to index");
        return;
    }

    println!("Indexing {} papers", papers.len());
    let client = Client::new(
        "http://localhost:7700",
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
    if page.is_empty() {
        return None;
    }

    let html = page.get_html();

    let mut hasher: DefaultHasher = DefaultHasher::new();

    let document = scraper::Html::parse_document(&html);
    let mut title = page.get_url().to_string();
    for selector in paper.get_selectors() {
        let texts = document
            .select(selector)
            .filter(|element| {
                let name = element.value().name();
                name != "style" && name != "script"
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
            hash_url: hasher.finish(),
        });
    }
    None
}

#[tokio::main]
async fn main() {
    let file = std::fs::File::open("newspapers.json").unwrap();
    let newspapers: Vec<NewspaperModel> = serde_json::from_reader(file).unwrap();

    let newspapers = newspapers
        .iter()
        .map(|newspaper| Newspaper::from(newspaper.clone()))
        .collect::<Vec<_>>();

    for paper in newspapers {
        let mut website = Website::new(paper.get_url());
        website.with_limit(1);
        website.with_delay(18);
        let mut rx2 = website.subscribe(0).unwrap(); // Corrected buffer size
        println!("Scraping {}", paper.get_title());
        let join_handle = tokio::spawn(async move {
            const MAX_PAPERS: usize = 80;
            let mut papers = Vec::with_capacity(MAX_PAPERS);
            while let Ok(page) = rx2.recv().await {
                println!("page");
                if let Some(paper) = process_page(page, &paper).await {
                    papers.push(paper);
                    if papers.len() >= MAX_PAPERS {
                        indexing(papers.as_slice()).await;
                        papers.clear();
                    }
                }
            }
            if !papers.is_empty() {
                indexing(papers.as_slice()).await;
            }
            println!("Done scraping {}", paper.get_title());
        });
        website.scrape().await; 
        website.unsubscribe();
        join_handle.await.unwrap();
    }
}
