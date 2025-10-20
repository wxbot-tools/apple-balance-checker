import os

port=8080
exec_dir = os.path.dirname(os.path.abspath(__file__))
balance_checker_accounts_file = os.path.join(exec_dir, 'balance_check_accounts.json')
proxy_config_file = os.path.join(exec_dir, 'proxy_config.json')

