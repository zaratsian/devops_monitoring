import sys
import asyncio
import aiohttp


def get_linux_hosts(file='hosts.config'):
    '''
        hosts.config contains a newline seperated list of linux hosts
    '''
    data = open(file,'r').read()
    hosts = [host for host in data.split('\n') if host != '']
    return hosts


async def get(
    session: aiohttp.ClientSession,
    host: str,
    **kwargs
) -> dict:
    url = f"http://{host}:9090/metrics"
    print(f"Requesting {url}")
    resp = await session.request('GET', url=url, **kwargs)
    data = await resp.text()
    print(f"Received data for {url}")
    return data


async def main(hosts, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for host in hosts:
            tasks.append(get(session=session, host=host, **kwargs))
        
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


if __name__ == '__main__':
    hosts = get_linux_hosts(file='hosts.config') # ['35.209.55.192', '35.208.247.167', '35.209.3.73']
    metrics = asyncio.run(main(hosts))
    # Write "metrics" to database, push via HTTP to listener (ie. Prometheus PushGateway), or expose via endpoint where the metrics can be scraped. 

#ZEND
