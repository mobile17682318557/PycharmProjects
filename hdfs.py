import pyhdfs
ps=pyhdfs.HdfsClient('192.168.18.5,50070',user_name='root')
response=ps.copy_to_local('/user/root/data.txt','F:/data.txt')