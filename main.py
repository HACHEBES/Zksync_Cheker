from aiohttp import ClientSession
import asyncio
async def trans_balance(session: ClientSession,address):

    try:
        async with session.get(f'https://block-explorer-api.mainnet.zksync.io/address/{address}') as response_trans:
            response_trans_json = await response_trans.json()
            trans = response_trans_json['sealedNonce']
            balance = float(response_trans_json['balances']['0x000000000000000000000000000000000000800A']['balance'])/10**18
            return trans, balance
    except Exception as e:
        print('Фейл')
        return 0,0
async def date(session: ClientSession, address):

    params = {
        'address': f'{address}',
        'pageSize': '10',
        'page': '1',
    }
    try:
        async with session.get('https://block-explorer-api.mainnet.zksync.io/transactions',params=params) as response_time:
            response_time_json = await response_time.json()
            time = response_time_json['items']
            time = time[0]['receivedAt'].split('T')
            return time[0]
    except Exception as e:
        print('Фейл')
        return 0
async def cheker(session: ClientSession, address):

    balances, time = await asyncio.gather(trans_balance(session, address=address),date(session, address=address))
    return f'{balances[1]}:{balances[0]}:{time}'
async def main():

    addresses = []
    with open('wallets.txt', 'r') as file:
        for line in file:
            addresses.append(line.strip())
    async with ClientSession() as session:
        tasks = [cheker(session, address) for address in addresses]
        results = await asyncio.gather(*tasks)
        with open('output.txt', 'w') as file:
            file.write('')
        for i in range(len(addresses)):
            with open('output.txt', 'a') as file:
                data = f'{addresses[i]}:{results[i]}'
                file.write(data + '\n')
        return results

asyncio.run(main())