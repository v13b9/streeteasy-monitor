from src.streeteasymonitor.monitor import Monitor

default = {

    'min_price': 0,
    'max_price': 2900,
    'min_beds': 1,
    'max_beds': 3,

    'areas': [
        'Carroll Gardens',
        'Clinton Hill',
        'Cobble Hill',
        # 'Crown Heights',
        'Fort Greene',
        'Gowanus',
        'Greenpoint',
        'Park Slope',
        'Prospect Heights',
        # 'Prospect Lefferts Gardens',
        'Williamsburg',
        'Bedford-Stuyvesant',
        'Boerum Hill',
        'DUMBO',
        'Downtown Brooklyn',
        # 'Ridgewood',
        'Brooklyn Heights',
        # 'Lower East Side',
        'Upper East Side',
    ]

}

def main(**kwargs):
    with Monitor(**kwargs) as monitor:
        monitor.run()


if __name__ == '__main__':
    main(**default)
