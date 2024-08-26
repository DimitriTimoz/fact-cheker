use scraper::Selector;
use serde::{Deserialize, Serialize};
use spider::url::Url;


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NewspaperModel {
    title: String,
    url: String,
    selectors: Vec<String>,
}

#[derive(Debug)]
pub struct Newspaper {
    title: String,
    url: Url,
    selectors: Vec<Selector>,
}


impl From<NewspaperModel> for Newspaper {
    fn from(model: NewspaperModel) -> Self {
        let mut selectors = Vec::new();
        for selector in model.selectors {
            selectors.push(Selector::parse(&selector).unwrap());
        }
        Newspaper {
            title: model.title,
            url: Url::parse(&model.url).unwrap(),
            selectors,
        }
    }
}

impl Newspaper {
    pub fn new(title: String, url: Url, selectors: Vec<Selector>) -> Self {
        Newspaper {
            title,
            url,
            selectors,
        }
    }

    pub fn get_title(&self) -> &str {
        &self.title
    }

    pub fn get_url(&self) -> &Url {
        &self.url
    }

    pub fn get_selectors(&self) -> &Vec<Selector> {
        &self.selectors
    }
}
