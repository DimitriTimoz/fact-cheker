use scraper::Selector;
use serde_derive::{Deserialize, Serialize};
//use spider::url::Url;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NewspaperModel {
    title: String,
    url: String,
    selectors: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct Newspaper {
    title: String,
    url: String,
    selectors: Vec<Selector>,
}

impl From<NewspaperModel> for Newspaper {
    fn from(model: NewspaperModel) -> Self {
        let mut selectors = Vec::new();
        for selector in model.selectors {
            selectors.push(Selector::parse(&format!("{} :not(script):not(style)", selector)).unwrap());
        }
        Newspaper {
            title: model.title,
            url: model.url,
            selectors,
        }
    }
}

impl Newspaper {
    pub fn new(title: String, url: String, selectors: Vec<Selector>) -> Self {
        Newspaper {
            title,
            url,
            selectors,
        }
    }

    pub fn get_title(&self) -> &str {
        &self.title
    }

    pub fn get_url(&self) -> &str {
        &self.url
    }

    pub fn get_selectors(&self) -> &Vec<Selector> {
        &self.selectors
    }
}

#[derive(Serialize, Deserialize)]
pub struct Paper {
    pub title: String,
    pub url: String,
    pub hash_url: String,
    pub content: String,
}
