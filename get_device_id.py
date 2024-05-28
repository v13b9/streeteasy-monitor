        # print(f'\nTrying GET {listing['url']}...')
        # wait()
        # r = s.get(listing['url'])
        # print(f'Status code: {r.status_code} {r.reason}')

        # soup = BeautifulSoup(r.content, 'html.parser')
        # # find more robust solution
        # script = soup('script')[-2].string
        # pattern = r'(?<=deviceId\:\s\")[a-zA-Z0-9-]*(?=\",)'
        # deviceId = re.search(pattern, script).group()

        # print('deviceId:', deviceId)