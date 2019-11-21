from conf import env_conf
import subprocess as commands


def install():
    deploy_file = env_conf.root_dir + "/deploy/kfserving.yaml"
    cmd = "kubectl create -f " + deploy_file
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)


if __name__ == '__main__':
    install()
