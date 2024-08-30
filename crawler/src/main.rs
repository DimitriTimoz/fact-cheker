use spider::url::Url;
use std::hash::{DefaultHasher, Hash, Hasher};

use newspaper::{Newspaper, NewspaperModel, Paper};
use spider::website::Website;
use spider::tokio;

use meilisearch_sdk::client::*;
  
pub mod newspaper;

async fn indexing(papers: &[Paper]) {
    println!("Indexing {} papers", papers.len());
    let client = Client::new("http://localhost:7700", Some("R5K9sb6KbsnAIEuR97mFrHMEEQ4oBjWAlWZcv9OeN70")).unwrap();

    let res = client.index("papers").add_documents(papers, Some("hash_url")).await;
    match res {
        Ok(_) => println!("Indexing done"),
        Err(e) => println!("Error: {}", e),
    }
}

async fn process_page(html: String, paper: &Newspaper) -> Option<Paper> {
    let mut hasher: DefaultHasher = DefaultHasher::new();

    let document = scraper::Html::parse_document(&html);
    for selector in paper.get_selectors() {
        let texts = document.select(selector).flat_map(|el| el.text()).collect::<Vec<_>>();
        if texts.is_empty() {
            continue;
        }
        paper.get_url().hash(&mut hasher);
        return Some(Paper {
            title: paper.get_url().to_string(),
            url: paper.get_url().to_string(),
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

    let newspapers = newspapers.iter().map(|newspaper| Newspaper::from(newspaper.clone())).collect::<Vec<_>>();
    // TODO: Use a thread pool to scrape multiple websites concurrently
    for paper in newspapers {
        let mut website = Website::new(paper.get_url().as_str());
        website.with_limit(100000);
        let mut rx2 = website.subscribe(0).unwrap();
        println!("Scraping {}", paper.get_title());
        tokio::spawn(async move {
            const MAX_PAPERS: usize = 64;
            let mut papers = Vec::with_capacity(MAX_PAPERS);
            while let Ok(page) = rx2.recv().await {
                println!("Page: {}", page.get_url());
                let html = page.get_html();

                if let Some(paper) = process_page(html, &paper).await {
                    papers.push(paper);
                    if papers.len() >= MAX_PAPERS {
                        indexing(papers.as_slice()).await;
                        papers.clear();
                        println!("After 1");
                    }
                }
                println!("After 2");
            }
            println!("After 3");
            if !papers.is_empty() {
                indexing(papers.as_slice()).await;
                papers.clear();
                println!("After panicked");
            }
        });
        println!("After 4");
        website.scrape().await;
        println!("Scraping done");
        //if papers.is_empty() {
         //   continue;
        //}*/
        //indexing(papers.as_slice()).await;
    }
}
