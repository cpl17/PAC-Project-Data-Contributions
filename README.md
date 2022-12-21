# PAC-Project-Data-Contributions

*CAD_BuildingNurseryDB* -> Scripts used scrape online nursery registries.

*CAD_NurseryInventory* -> TextFiles stores the text from a nursery's availability page (website, pdf, facebook post etc).
Matches are found using the two getmatches script (one for a single text file, one for all files in the folder). Output contains the matches in a long format (one instance for each match) and a wide format (one instance for each flower, columns are aggregated into list).

*ERA_DataExploration* -> Notebooks and scripts used to explore the source database.

*ERA_MissingData* -> Scripts and notebooks used to scrape various plant directories to fill in missing values in the source db.

*OnlineAvailability* -> Scripts used to scrape online directories to build out our online availability feature.
