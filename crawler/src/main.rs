    use std::hash::{DefaultHasher, Hash, Hasher};

    use newspaper::{Newspaper, NewspaperModel, Paper};
    use spider::page::Page;
    use spider::website::Website;
    use spider::tokio;

    use meilisearch_sdk::client::*;
    
    pub mod newspaper;

    async fn indexing(papers: &[Paper]) {
        if papers.is_empty() {
            println!("No papers to index");
            return;
        }

        println!("Indexing {} papers", papers.len());
        let client = Client::new("http://localhost:7700", Some("R5K9sb6KbsnAIEuR97mFrHMEEQ4oBjWAlWZcv9OeN70")).unwrap();

        match client.index("papers").add_documents(papers, Some("hash_url")).await {
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
        for selector in paper.get_selectors() {
            let texts = document.select(selector)
            .filter(|element| {
                let name = element.value().name();
                name != "style" && name != "script"
            })
            .flat_map(|el| el.text())
            .collect::<Vec<_>>();
            if texts.is_empty() {
                continue;
            }
            page.get_url().hash(&mut hasher);
            return Some(Paper {
                title: page.get_url().to_string(),
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

        let newspapers = newspapers.iter().map(|newspaper| Newspaper::from(newspaper.clone())).collect::<Vec<_>>();

        for paper in newspapers {
            let mut website = Website::new(paper.get_url());
            website.with_delay(20);
            website.with_limit(50_000);
            let mut rx2 = website.subscribe(32).unwrap();
            println!("Scraping {}", paper.get_title());
            let scrapper = website.scrape_smart();
            let indexer = tokio::spawn(async move {
                const MAX_PAPERS: usize = 64;
                let mut papers = Vec::with_capacity(MAX_PAPERS);
                loop {
                    let page = rx2.recv().await;
                    match page {
                        Err(e) => println!("Error: {}", e),
                        Ok(page) => {
                            if page.is_empty() {
                                continue;
                            }
                            if let Some(paper) = process_page(page, &paper).await {
                                papers.push(paper);
                                if papers.len() >= MAX_PAPERS {
                                    indexing(papers.as_slice()).await;
                                    papers.clear();
                                }
                            }
                        }
                            
                    }
                }
            });
            let _ = futures::join!(scrapper, indexer);
            website.unsubscribe();
        }
    }
