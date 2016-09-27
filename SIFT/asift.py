#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Affine invariant feature-based image matching sample.

This sample is similar to find_obj.py, but uses the affine transformation
space sampling technique, called ASIFT [1]. While the original implementation
is based on SIFT, you can try to use SURF or ORB detectors instead. Homography RANSAC
is used to reject outliers. Threading is used for faster affine sampling.

[1] http://www.ipol.im/pub/algo/my_affine_sift/

USAGE
  asift.py [--feature=<sift|surf|orb>[-flann]] [ <image1> <image2> ]

  --feature  - Feature to use. Can be sift, surf of orb. Append '-flann' to feature name
                to use Flann-based matcher instead bruteforce.

  Press left mouse button on a feature point to see its matching point.
'''

from multiprocessing.pool import ThreadPool
import time
import cPickle as pickle
from datetime import datetime
import codecs

from detect import *
from common import Timer
from find_obj import init_feature, filter_matches
from SIFT.featureIO import *

logos = ['Acura讴歌','Armani阿玛尼','AstonMartin阿斯顿马丁','Audi奥迪','AZIMUT阿兹慕','Balenciaga巴黎世家',
         'Bally巴利','Beneteau博纳多','Bentley宾利','Benz奔驰','Biotherm碧欧泉','Blumarine蓝色情人','BMW宝马',
         'Bombardier庞巴迪','Bottega Veneta宝缇嘉','Braastad宝伯特','Bucherer宝齐莱','Bulgari宝格丽',
         'BURBERRY巴宝莉','Cartier卡地亚','Celine赛琳','Cessna赛斯纳','CHANEL香奈儿','Chevrolet雪佛兰',
         'Chopard萧邦','Cirrus西锐','CK卡文克莱','Coach蔻驰','Constant康斯登','Damiani德米亚尼','De Beers戴比尔斯',
         'Dior迪奥','DKNY','Estee Lauder雅诗兰黛','Feadship斐帝星','Fendi芬迪','Ferragamo菲拉格慕','Ferrari法拉利',
         'Franck Muller法穆兰','Furla芙拉','Galtiscopio卡比奥','Givenchy纪梵希','Glashutte格拉苏蒂','GUCCI古驰','GUESS',
         'Gulfstream湾流','hamilton汉米尔顿','HERMES爱马仕','Hublot宇舶','Infiniti英菲尼迪','IWC万国表','Jaeger积家',
         'Jaguar捷豹','Jeanneau亚诺','Lafite拉菲','Lamborghini兰博基尼','Lancome兰蔻','Landrover路虎','Lexus雷克萨斯',
         'Longines浪琴','LOTOS','LV路易威登','Martell马爹利','Maserati玛莎拉蒂','Mclaren迈凯轮','MIDO美度','Mikimoto御木本',
         'Milus美力士','MiuMiu缪缪','Montblanc万宝龙','Nina Ricci莲娜丽姿','OMEGA欧米茄','Panerai沛纳海',
         'PatekPhilippe百达翡丽','Piaget伯爵','Pomellato宝曼兰朵','Porsche保时捷','PRADA普拉达','Rado雷达',
         'RaymondWeil蕾蒙威','Raytheon雷神','Rolex劳力士','Rollsroyce劳斯莱斯','Swarovski施华洛世奇','TAG Heuer豪雅',
         'Tiffany蒂芙尼','Tissot天梭','Titoni梅花','TSL谢瑞麟','VanCleefArpels梵克雅宝','VeraWang王薇薇','Volvo沃尔沃',
         'Wally沃利','YSL圣罗兰','三宅一生','名士','太子珠宝','江诗丹顿','灰雁伏特加','维多利亚的秘密','芝柏GP','高缇耶']


class img_search:

    def __init__(self, name):
        self.alg = name
        self.keypoints_database = None

    def search(self, fn1):
        if self.keypoints_database == None:
            start_time = datetime.now()
            print 'loading training file', datetime.now()
            self.keypoints_database = pickle.load(open("./feature/keypoints_database_"+self.alg+".p", "rb"))
            print 'load complete cost:', datetime.now() - start_time

        import sys, getopt
        opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
        opts = dict(opts)
        # feature_name = opts.get('--feature', 'sift-flann')
        feature_name = opts.get('--feature', self.alg+'-flann')
        fn2 = './img/LV路易威登.jpg'
        img1 = cv2.imread(fn1, 0)

        imgt = cv2.imread(fn2, 0)
        # img2 = cv2.imread(img1)
        detector, matcher = init_feature(feature_name)
        # print detector, '123123'

        if detector is not None:
            print 'using', feature_name
        else:
            print 'unknown feature:', feature_name
            sys.exit(1)

        pool = ThreadPool(processes = cv2.getNumberOfCPUs())
        try:
            kp1, desc1 = affine_detect(detector, img1, pool=pool)
        except:
            return '0'

        results = []

        def match_and_draw(win, kpa, desca3):
            with Timer('matching'):
                raw_matches = matcher.knnMatch(desc1, trainDescriptors=desca3, k=2) #2
            p1, p2, kp_pairs = filter_matches(kp1, kpa, raw_matches)
            if len(p1) > 4:
                H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
                print '%d / %d  inliers/matched' % (np.sum(status), len(status))
                # do not draw outliers (there will be a lot of them)
                kp_pairs = [kpp for kpp, flag in zip(kp_pairs, status) if flag]
                return win, kp_pairs, H, (np.sum(status))
            else:
                return win, kp_pairs, None, -1

        start_m = datetime.now()
        for keypoints_data in self.keypoints_database:
            kp3, desc3, name, path = unpickle_keypoints(keypoints_data)
            try:
                win, kp_pairs, H, num = match_and_draw('affine find_obj', kp3, desc3)
                result = {'win': win, 'name': name[0], 'path': path[0], 'kp_pairs': kp_pairs, 'num': num, 'H': H}
                results.append(result)
            except:
                print name, 'error!'
        print 'match finish: ', datetime.now() - start_m
        results.sort(reverse=True, key=lambda x: x['num'])
        results = self.get_result(results)

        for i in results:
            print i
        return results[0]['name']

    def training(self):
        # save training data
        import glob, sys, getopt
        opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
        opts = dict(opts)
        feature_name = opts.get('--feature', self.alg+'-flann')
        detector, matcher = init_feature(feature_name)
        if detector!=None:
            print 'using', feature_name
        else:
            print 'unknown feature:', feature_name
            sys.exit(1)

        pool = ThreadPool(processes=cv2.getNumberOfCPUs())
        print 'start'
        icc = 0
        temp_array = []
        errors = []
        for imagePath in glob.glob("./collect_bi/*.*"):
            imageName = imagePath[imagePath.rfind("/") + 1:imagePath.rfind(".")]
            image = cv2.imread(imagePath)
            print imageName
            try:
                kp, desc = affine_detect(detector, image, pool=pool)
                temp = pickle_keypoints(kp, desc, imageName, imagePath)
                temp_array.append(temp)
                icc += 1
                print icc, imageName
            except:
                errors.append(imageName)
            time.sleep(0.3)
            if icc > 1050:
                # time.sleep(1)
                break
            else:
                time.sleep(1)
        pickle.dump(temp_array, open("./feature/keypoints_database_"+self.alg+".p", "wb"))
        print 'error!!!'
        for i in errors:
            print i
        print 'successful finish'
        # end save\

    def add_data(self, num, inter=49):

        temp_array = pickle.load(open("./feature/keypoints_database_"+self.alg+".p", "rb"))
        # save training data
        import glob, sys, getopt

        opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
        opts = dict(opts)

        feature_name = opts.get('--feature', self.alg+'-flann')
        detector, matcher = init_feature(feature_name)

        if detector is not None:
            print 'using', feature_name
        else:
            print 'unknown feature:', feature_name
            sys.exit(1)

        pool = ThreadPool(processes=cv2.getNumberOfCPUs())
        print 'start'
        icc = 0
        errors = []
        k = 0
        for imagePath in glob.glob("./collect_bi/*.*"):
            k+=1
            if k > num:
                imageName = imagePath[imagePath.rfind("/") + 1:imagePath.rfind(".")]
                image = cv2.imread(imagePath)
                print imageName
                try:
                    kp, desc = affine_detect(detector, image, pool=pool)
                    temp = pickle_keypoints(kp, desc, imageName, imagePath)
                    temp_array.append(temp)
                    icc += 1
                    print icc, imageName
                except:
                    errors.append(imageName)
                time.sleep(0.1)
                if k-num > inter:
                    break
                    # time.sleep(1)
                else:
                    time.sleep(1)

        pickle.dump(temp_array, open("./feature/keypoints_database_"+self.alg+".p", "wb"))
        print 'error!!!'
        for i in errors:
            print i
        print 'successful finish'
        # end save\

    def get_result(self, results):

        k = 0
        re = {}
        rea = []

        for r in results:

            if get_name(r['name']) in re.keys():
                re[get_name(r['name'])] += 1
            else:
                re[get_name(r['name'])] = 1
            k += 1
            if k > 3:
                break

        for k in re.keys():
            rea.append({'name': k, 'count': re[k]})
        rea.sort(reverse=True, key=lambda x: x['count'])

        return rea


def test(alg, min=0):

    file = codecs.open('test.txt', 'ab', encoding='utf-8')
    sift = img_search(alg)

    import glob
    total = 0.0
    correct = 0.0
    start_test = datetime.now()

    print "start testing!"
    line = "start testing! " + str(start_test) + '\n'
    file.write(line.decode("unicode_escape"))
    num = 0

    for imagePath in glob.glob("./test_img3_bi/*.*"):
        num += 1
        if num > min:
            try:

                imagename = imagePath[imagePath.rfind("/") + 1:imagePath.rfind(".")]
                imageName = get_name(imagename)

                print 'matching', imagePath
                line = "matching "+imagePath + str(datetime.now())+'\n'
                file.write(line.decode("unicode_escape"))
                start_time = datetime.now()
                result = sift.search(imagePath)

                if result != '0':
                    total += 1.0

                print 'match', imageName, result
                print 'match finish cost:', datetime.now() - start_time
                line = "match "+imagePath+' '+result+' '+str(datetime.now())+'\n'

                file.write(line.decode("unicode_escape"))
                if imageName == result:
                    correct += 1.0
                    print 'correct'

            except:
                print imagePath
                line = "error "+imagePath+' '+str(datetime.now())+'\n'
                file.write(line.decode("unicode_escape"))

        if num - min > 50:
            break

    print 'total:', total, 'correct', correct
    print 'correct percent:', float(correct)/total
    print 'cost time', datetime.now() - start_test
    percent = correct/total
    line = "total: "+total+" correct percent: "+bytes(percent)+' '+str(datetime.now())+' cost time '+str(datetime.now() - start_test)+ '\n'
    file.write(line.decode("unicode_escape"))


if __name__ == '__main__':
    test('sift')
