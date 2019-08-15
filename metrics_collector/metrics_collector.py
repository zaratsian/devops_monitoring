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
    data = {'host':host, 'metrics': await resp.text()}
    print(f"Received data for {url}")
    return data


async def main(hosts, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for host in hosts:
            tasks.append(get(session=session, host=host, **kwargs))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


if __name__ == '__main__':
    hosts = get_linux_hosts(file='hosts.config') # hosts = ['35.209.55.192', '35.208.247.167', '35.209.3.73']
    metrics = asyncio.run(main(hosts))
    # From this point, "metrics" could be written to a database, pushed via HTTP to listener (ie. Prometheus PushGateway), or exposed via endpoint where the metrics can be scraped. 

'''
Below is an example output from "metrics" for a single host in the list.
Note: metrics are newline seperated, which could be split by running .split('\n') if that is what is required for insert into a db for example.

>>> metrics[0]
{'host': '35.209.230.68', 'metrics': 'gce_memory_total 0.358\ngce_process_systemd_memory 1.1043\ngce_process_kthreadd_memory 0.0\ngce_process_ksoftirqd_0_memory 0.0\ngce_process_kworker_0_0H_memory 0.0\ngce_process_kworker_u2_0_memory 0.0\ngce_process_rcu_sched_memory 0.0\ngce_process_rcu_bh_memory 0.0\ngce_process_migration_0_memory 0.0\ngce_process_lru_add_drain_memory 0.0\ngce_process_watchdog_0_memory 0.0\ngce_process_cpuhp_0_memory 0.0\ngce_process_kdevtmpfs_memory 0.0\ngce_process_netns_memory 0.0\ngce_process_khungtaskd_memory 0.0\ngce_process_oom_reaper_memory 0.0\ngce_process_writeback_memory 0.0\ngce_process_kcompactd0_memory 0.0\ngce_process_ksmd_memory 0.0\ngce_process_khugepaged_memory 0.0\ngce_process_crypto_memory 0.0\ngce_process_kintegrityd_memory 0.0\ngce_process_bioset_memory 0.0\ngce_process_kblockd_memory 0.0\ngce_process_devfreq_wq_memory 0.0\ngce_process_watchdogd_memory 0.0\ngce_process_kworker_u2_1_memory 0.0\ngce_process_kswapd0_memory 0.0\ngce_process_vmstat_memory 0.0\ngce_process_kthrotld_memory 0.0\ngce_process_ipv6_addrconf_memory 0.0\ngce_process_scsi_eh_0_memory 0.0\ngce_process_scsi_tmf_0_memory 0.0\ngce_process_bioset_memory 0.0\ngce_process_kworker_u3_0_memory 0.0\ngce_process_kworker_0_1H_memory 0.0\ngce_process_jbd2_sda1_8_memory 0.0\ngce_process_ext4_rsv_conver_memory 0.0\ngce_process_systemd_journald_memory 0.8439\ngce_process_kauditd_memory 0.0\ngce_process_systemd_udevd_memory 0.6\ngce_process_acpid_memory 0.1859\ngce_process_cron_memory 0.4556\ngce_process_edac_poller_memory 0.0\ngce_process_rsyslogd_memory 0.4905\ngce_process_dhclient_memory 0.4721\ngce_process_agetty_memory 0.2875\ngce_process_agetty_memory 0.2828\ngce_process_agetty_memory 0.2855\ngce_process_agetty_memory 0.2703\ngce_process_agetty_memory 0.2835\ngce_process_agetty_memory 0.2822\ngce_process_agetty_memory 0.3343\ngce_process_ntpd_memory 0.6817\ngce_process_google_network__memory 3.8008\ngce_process_google_metadata_memory 3.7646\ngce_process_google_clock_sk_memory 3.7659\ngce_process_google_accounts_memory 3.8305\ngce_process_sshd_memory 0.8881\ngce_process_tmp580283ci_memory 0.0\ngce_process_python_memory 3.8279\ngce_process_kworker_0_2_memory 0.0\ngce_process_kworker_0_1_memory 0.0'}

'''

#ZEND
