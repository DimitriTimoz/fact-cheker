extern crate spider;

use futures::executor::block_on;
use newspaper::{Newspaper, NewspaperModel, Paper};
use spider::website::Website;
use spider::tokio;

use meilisearch_sdk::{
    indexes::*,
    client::*,
    search::*,
    settings::*
  };
  
pub mod newspaper;


#[tokio::main]
async fn main() {
    let file = std::fs::File::open("newspapers.json").unwrap();
    let newspapers: Vec<NewspaperModel> = serde_json::from_reader(file).unwrap();

    let newspapers = newspapers.iter().map(|newspaper| Newspaper::from(newspaper.clone())).collect::<Vec<_>>();

    for paper in newspapers {
       let mut website = Website::new(paper.get_url().as_str());
        website.with_depth(7);
        website.with_limit(100);
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
                        println!("Selector found");
                        if text.is_empty() {
                            continue;
                        }
                        
                        papers.push(Paper {
                            title: page.get_url().to_string(),
                            url: page.get_url().to_string(),
                            content: text.join(" "),
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
            let client = Client::new("http://localhost:7700", Some("")).unwrap();

            let res = client.index("papers").add_documents(&papers, Some("url")).await;
            match res {
                Ok(_) => println!("Indexing done"),
                Err(e) => println!("Error: {}", e),
            }

        });
    }
}
