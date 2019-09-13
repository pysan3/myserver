import apps.app as backapp

print(backapp.run_command(1, 'new', 'python test_dir/itoi.py'.split()).stdout.decode('utf-8'))

c = backapp.Color('#c6e48b')
for i in range(3):
    c.darken(1)
    print(c.return_colorcode())
