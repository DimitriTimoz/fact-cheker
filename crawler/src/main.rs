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
    .filter_or("RUST_LOG", "error")
    .write_style_or("RUST_LOG_STYLE", "always");

    env_logger::init_from_env(env);

    let file = std::fs::File::open("newspapers.json").unwrap();
    let newspapers: Vec<NewspaperModel> = serde_json::from_reader(file).unwrap();

    let newspapers = newspapers.iter().map(|newspaper| Newspaper::from(newspaper.clone())).collect::<Vec<_>>();
    let mut hasher: DefaultHasher = DefaultHasher::new();
    // TODO: Use a thread pool to scrape multiple websites concurrently
    for paper in newspapers {
       let mut website = Website::new(paper.get_url().as_str());
        website.with_limit(10_000);
        println!("Scraping {}", paper.get_title());
        website.scrape().await;
        println!("Scraping done");
        let mut papers = Vec::new();
        if let Some(pages) = website.get_pages() {
            println!("Scraping pages");
            for page in pages.as_ref() {
                let html = page.get_html();
                println!("Scraping page");
                let document = scraper::Html::parse_fragment(&html);
                println!("doc scraped");
                for selector in paper.get_selectors() {
                    let texts = document.select(selector).flat_map(|el| el.text()).collect::<Vec<_>>();
                    if texts.is_empty() {
                        continue;
                    }
                    page.get_url().hash(&mut hasher);
                    papers.push(Paper {
                        title: page.get_url().to_string(),
                        url: page.get_url().to_string(),
                        content: texts.join(" "),
                        hash_url: hasher.finish()
                    });
                    break;    
                }
            }
        }
        if papers.is_empty() {
            continue;
        }
        println!("Indexing {} papers", papers.len());
        block_on(async move {
            let client = Client::new("http://localhost:7700", Some("tApGJDuzRwoxlq8GAJq6FhgSHytT68bjtDYDaxY41s0")).unwrap();

            let res = client.index("papers").add_documents(&papers, Some("hash_url")).await;
            match res {
                Ok(_) => println!("Indexing done"),
                Err(e) => println!("Error: {}", e),
            }
        });
    }
}
