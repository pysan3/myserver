import apps.app as backapp

print(backapp.run_command(1, 'new', 'python test_dir/itoi.py'.split()).stdout.decode('utf-8'))