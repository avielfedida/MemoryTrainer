from db_manager import DbManager

records = [
    {
        'category': 'blockchain',
        'term': 'PoS',
        'answer': 'yoooooooooooooooooooooooooooo'
    },
    {
        'category': 'blockchain',
        'term': 'PoW',
        'answer': 'boooooooooooooooooooooo'
    },
    {
        'category': 'blockchain',
        'term': 'Bitcoin',
        'answer': 'doooooooooooooooooooooo'
    },
    {
        'category': 'blockchain',
        'term': 'ETH',
        'answer': 'mooooooooooooooooooooooooooo'
    },
    {
        'category': 'blockchain',
        'term': 'Decentralization',
        'answer': 'qoooooooooooooooooooooooo'
    },
    {
        'category': 'blockchain',
        'term': 'P2P',
        'answer': 'wqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'PoB',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Monero',
        'answer': 'wwwwwwwwwwwwwwwwwwww'
    },
    {
        'category': 'blockchain',
        'term': 'Bitcoin cash',
        'answer': 'mmmmmmmmmmmmmmmmmmmmm'
    },
    {
        'category': 'blockchain',
        'term': 'Bitcoin gold',
        'answer': 'goooooooooooooooooooooooooooooo'
    },
    {
        'category': 'blockchain',
        'term': 'Coinbase',
        'answer': 'ewwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    },
    {
        'category': 'blockchain',
        'term': 'Mining',
        'answer': 'qwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
    },
    {
        'category': 'blockchain',
        'term': 'PoA',
        'answer': 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
    },
    {
        'category': 'blockchain',
        'term': 'DPoS',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Transaction',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Linked list',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Merkle tree',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Patricia tree',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Distributed Hash tables',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Bloom filter',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Hashcash',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    },
    {
        'category': 'blockchain',
        'term': 'Token',
        'answer': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    }
]

dbManager = DbManager()

for idx, rec in enumerate(records):
    with dbManager.conn:
        c = dbManager.conn.cursor()
        c.execute("""
        INSERT INTO Terms (category, term, answer, appeared, wrong, insert_time) VALUES 
        (?, ?, ?, ?, ?, datetime('now', 'localtime'))
        """, (str.lower(rec.get('category')), str.lower(rec.get('term')), str.lower(rec.get('answer')), 2, 1))


