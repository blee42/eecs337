# Golden Globes Tweet Parser

Project by Kevin Chen, Brittany Lee, Kevin Broh-Kahn, and Bhavita Jaiswal.

## Team notes

2/6/2015 Update:
Added scraper for all categories and nominees. `get_categories` will return data in this form:

`
[
    {
        'category': 'award1',
        'nominees': 
            [
                'nominee1',
                'nominee2',
                '...'
            ]
    },

    {
        'category': 'award2',
        'nominees': 
            [
                'nominee1',
                'nominee2',
                '...'
            ]
    },
]
`

I did not scrape the two hosts -- didn't seem to be worth it.

