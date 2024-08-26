extern crate spider;

use newspaper::{Newspaper, NewspaperModel};
use spider::website::Website;
use spider::tokio;

pub mod newspaper;


#[tokio::main]
async fn main() {

    let file = std::fs::File::open("newspapers.json").unwrap();
    let newspapers: Vec<NewspaperModel> = serde_json::from_reader(file).unwrap();

    let newspapers = newspapers.iter().map(|newspaper| Newspaper::from(newspaper.clone())).collect::<Vec<_>>();
   

    for paper in newspapers {
       let mut website = Website::new(paper.get_url().as_str());
        website.with_limit(100);
        website.scrape().await;
    
        if let Some(pages) = website.get_pages() {
            for page in pages.as_ref() {
                let html = page.get_html();
                let document = scraper::Html::parse_document(&html);
                for selector in paper.get_selectors() {
                    let frag = document.select(selector).next();
                    if let Some(frag) = frag {
                        let text = frag.text().collect::<Vec<_>>();
                        if text.is_empty() {
                            continue;
                        }
                        println!("{:?}", text);
                        break;    
                    }
                }
            }
        }
    }
}
