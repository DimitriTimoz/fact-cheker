extern crate spider;
extern crate env_logger;

use std::hash::{DefaultHasher, Hash, Hasher};

use futures::executor::block_on;
use newspaper::{Newspaper, NewspaperModel, Paper};
use spider::website::Website;
use spider::tokio;
use env_logger::Env;

use meilisearch_sdk::client::*;
  
pub mod newspaper;


#[tokio::main]
async fn main() {
    let env = Env::default()
    .filter_or("RUST_LOG", "warn")
    .write_style_or("RUST_LOG_STYLE", "always");

    env_logger::init_from_env(env);

    let file = std::fs::File::open("newspapers.json").unwrap();
    let newspapers: Vec<NewspaperModel> = serde_json::from_reader(file).unwrap();

    let newspapers = newspapers.iter().map(|newspaper| Newspaper::from(newspaper.clone())).collect::<Vec<_>>();
    let mut hasher: DefaultHasher = DefaultHasher::new();
    // TODO: Use a thread pool to scrape multiple websites concurrently
    for paper in newspapers {
       let mut website = Website::new(paper.get_url().as_str());
        website.with_limit(10000);
        println!("Scraping {}", paper.get_title());
        website.scrape().await;
        println!("Scraping done");
        let mut papers = Vec::new();
        if let Some(pages) = website.get_pages() {
            for page in pages.as_ref() {
                let html = page.get_html();
                let document = scraper::Html::parse_fragment(&html);
                for selector in paper.get_selectors() {
                    let frag = document.select(selector).next();
                    if let Some(frag) = frag {
                        let text = frag.text().collect::<Vec<_>>();
                        if text.is_empty() {
                            continue;
                        }
                        page.get_url().hash(&mut hasher);
                        papers.push(Paper {
                            title: page.get_url().to_string(),
                            url: page.get_url().to_string(),
                            content: text.join(" "),
                            hash_url: hasher.finish()
                        });
                        break;    
                    }
                }
            }
        }
        if papers.is_empty() {
            continue;
        }
        println!("Indexing {} papers", papers.len());
        block_on(async move {
            let client = Client::new("http://localhost:7700", Some("p5nnddvyVWHDU-pBcD4QJTUGELtsLzgmA7eeU9M5eeA")).unwrap();

            let res = client.index("papers").add_documents(&papers, Some("hash_url")).await;
            match res {
                Ok(_) => println!("Indexing done"),
                Err(e) => println!("Error: {}", e),
            }
        });
    }
}
