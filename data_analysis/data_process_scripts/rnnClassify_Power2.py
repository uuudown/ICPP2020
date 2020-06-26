import os
import sys
import re
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import openpyxl
import pandas as pd
import math
import itertools
import matplotlib.patches as patches
import seaborn as sns
from decimal import Decimal
import glob
import csv
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import sklearn.svm
import sklearn.metrics
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
import tensorflow as tf
from tensorflow.keras import layers
import pickle
import random
import itertools

def get_app_list(fileName):
    """get metrics list

    Arguments:
        fileName {string} -- the file name of application file with absolute path

    Returns:
        app {list} -- the app  list
    """
    apps = []
    with open(fileName) as f:
        for line in f.readlines():
            if not line.startswith('#'):
                words = line.strip().split(',')
                app = words[0].strip()
                app_num = words[1].strip()
                apps.append([app, app_num])
        f.close()
    return apps

def load_file(filepath, max_len):
    dataframe = pd.read_csv(filepath, index_col=0)
    if (dataframe.shape[1] == 4 and dataframe.shape[0] > max_len):
        #if dataframe["u_gpu"].sum() == 0:
            #os.remove(filepath)
        #    print("none", filepath)
        #else:
        return dataframe.values[:max_len,:]
    else:
        print("wrong", filepath)

def load_group(arch, sample_rate):

    rate_len = {100:1800, 50:3600, 10:3600}
    max_len = rate_len[sample_rate]
    y_label = []
    app_label = []
    data_group = []
    category = "mybench"
    pathfolder = '/home/pzou/projects/Power_Signature/results-%d/%s/%s/power-combine'%(sample_rate, category, arch)
    app_list = app_list = get_app_list("/home/pzou/projects/Power_Signature/Scripts/applications-mem_%s.csv"%(category))
    for [app, app_num] in app_list:
        if arch=="k40" and "reductionMultiBlockCG" in app:
            continue
        fileName =app+app_num+"_res.csv"
        data = load_file(os.path.join(pathfolder, fileName), max_len)
        data_group.append(data)
        y_label.append(0)
    print("normal count", len(data_group))

    normal_count =len(data_group)
    category = "risky"
    pathfolder = '/home/pzou/projects/Power_Signature/results-%d/%s/%s/power-combine'%(sample_rate, category, arch)
    app_list = app_list = get_app_list("/home/pzou/projects/Power_Signature/Scripts/applications-mem_%s.csv"%(category))
    for [app, app_num] in app_list:
        fileName =app+app_num+"_res.csv"
        data = load_file(os.path.join(pathfolder, fileName), max_len)
        data_group.append(data)
        y_label.append(1)

    print("risk count", len(data_group)-normal_count)
    data_group = np.asarray(data_group)
    return data_group, y_label

def Index_split(index_label, model_eval):
    if model_eval == "seen":
        train_index5 = [355, 546, 7, 480, 279, 40, 140, 849, 738, 451, 477, 602, 143, 634, 347, 121, 757, 358, 150, 448, 702, 99, 805, 405, 635, 717, 574, 124, 642, 342, 577, 427, 141, 572, 166, 21, 794, 666, 599, 49, 283, 388, 689, 456, 588, 50, 450, 782, 454, 420, 309, 644, 26, 620, 253, 594, 686, 346, 730, 540, 272, 469, 240, 53, 555, 703, 806, 232, 155, 278, 370, 848, 300, 399, 518, 273, 62, 789, 811, 369, 330, 841, 443, 800, 111, 532, 673, 608, 843, 824, 445, 733, 509, 197, 583, 68, 483, 552, 680, 187, 470, 822, 313, 693, 652, 194, 765, 579, 224, 748, 51, 798, 242, 75, 219, 222, 385, 820, 696, 319, 513, 783, 4, 282, 6, 486, 248, 654, 15, 492, 562, 93, 318, 452, 56, 423, 517, 34, 426, 170, 747, 186, 10, 85, 580, 763, 325, 671, 115, 831, 189, 116, 419, 593, 57, 353, 438, 392, 481, 833, 259, 502, 336, 503, 125, 458, 357, 366, 46, 256, 106, 317, 821, 327, 617, 622, 576, 504, 780, 681, 741, 47, 157, 571, 468, 441, 234, 515, 668, 734, 626, 382, 218, 679, 674, 195, 90, 162, 246, 417, 54, 570, 636, 611, 16, 648, 464, 156, 505, 43, 510, 568, 591, 607, 512, 297, 305, 557, 612, 723, 573, 145, 790, 198, 812, 688, 495, 289, 650, 315, 514, 559, 98, 226, 801, 338, 381, 662, 303, 457, 772, 709, 277, 249, 321, 139, 746, 323, 436, 442, 127, 754, 554, 592, 533, 792, 762, 526, 846, 658, 361, 201, 541, 776, 556, 462, 537, 188, 409, 683, 732, 704, 128, 767, 122, 9, 604, 164, 292, 804, 851, 837, 101, 586, 351, 373, 59, 561, 48, 764, 721, 109, 810, 742, 133, 239, 422, 793, 76, 223, 544, 460, 311, 18, 191, 413, 663, 653, 280, 499, 328, 0, 563, 339, 182, 493, 839, 96, 55, 350, 39, 522, 761, 698, 304, 215, 298, 371, 538, 639, 237, 376, 88, 601, 529, 816, 268, 38, 152, 79, 429, 241, 781, 345, 174, 724, 506, 630, 24, 161, 119, 58, 262, 168, 81, 581, 813, 221, 756, 664, 647, 661, 83, 92, 301, 19, 558, 185, 227, 209, 333, 527, 231, 508, 428, 314, 836, 551, 238, 137, 25, 711, 753, 340, 61, 307, 158, 523, 471, 17, 67, 823, 627, 112, 705, 516, 785, 102, 415, 631, 487, 473, 619, 718, 291, 263, 251, 605, 678, 714, 1, 549, 375, 795, 643, 367, 402, 687, 2, 95, 535, 496, 778, 755, 284, 211, 410, 173, 287, 646, 142, 412, 192, 838, 401, 229, 712, 217, 597, 154, 430, 403, 181, 335, 751, 74, 414, 435, 852, 625, 640, 233, 20, 728, 750, 609, 589, 30, 290, 252, 69, 87, 114, 548, 91, 465, 167, 407, 616, 320, 784, 585, 77, 566, 531, 598, 690, 257, 255, 797, 497, 130, 100, 171, 796, 773, 453, 814, 655, 739, 200, 202, 660, 455, 633, 136, 520, 659, 569, 378, 706, 270, 606, 63, 393, 70, 534, 271, 543, 160, 845, 169, 36, 243, 82, 260, 372, 22, 337, 308, 826, 507, 220, 13, 819, 672, 584, 511, 177, 276, 547, 719, 476, 225, 632, 216, 29, 700, 722, 180, 745, 459, 766, 677, 638, 834, 474, 264, 64, 787, 214, 802, 786, 175, 398, 172, 332, 32, 31, 744, 235, 374, 397, 408, 699, 685, 418, 389, 817, 550, 265, 14, 94, 528, 391, 729, 78, 603, 387, 183, 449, 380, 491, 779, 190, 842, 621, 364, 135, 245, 274, 147, 105, 294, 324, 770, 799, 539, 691, 676, 110, 768, 5, 144, 103, 210, 446, 41, 362, 649, 377, 254, 146, 637, 86, 542, 431, 65, 715, 205, 44, 27, 80, 437, 113, 204, 519, 720, 670, 624, 411, 743, 740, 8, 73, 400, 118, 701, 206]
        test_index5 = [176, 444, 159, 299, 657, 463, 11, 352, 803, 844, 281, 384, 725, 489, 286, 213, 275, 827, 466, 316, 614, 500, 344, 258, 360, 193, 179, 682, 288, 692, 615, 28, 383, 461, 656, 363, 760, 567, 667, 396, 295, 395, 467, 472, 208, 302, 331, 695, 368, 808, 329, 354, 60, 769, 434, 613, 830, 587, 126, 12, 117, 736, 203, 840, 425, 341, 553, 322, 829, 365, 433, 488, 178, 138, 832, 228, 545, 394, 707, 148, 390, 536, 72, 71, 498, 269, 645, 348, 349, 809, 758, 479, 37, 791, 716, 23, 165, 84, 343, 818, 525, 684, 482, 582, 737, 835, 485, 236, 432, 247, 306, 669, 727, 475, 610, 296, 575, 752, 212, 775, 815, 759, 379, 406, 665, 807, 777, 261, 628, 675, 196, 641, 697, 440, 735, 771, 749, 828, 524, 521, 207, 774, 250, 310, 623, 424, 590, 494, 42, 151, 123, 850, 501, 134, 564, 52, 104, 3, 285, 708, 386, 199, 129, 312, 726, 490, 731, 359, 595, 266, 439, 847, 484, 108, 33, 132, 825, 651, 244, 66, 149, 131, 618, 713, 447, 694, 596, 629, 97, 560, 710, 184, 416, 788, 267, 153, 163, 404, 45, 478, 578, 120, 293, 89, 530, 107, 421, 600, 230, 326, 356, 35, 565, 334]

        train_index4 = [492, 473, 395, 444, 733, 328, 575, 273, 55, 702, 310, 747, 623, 402, 644, 163, 336, 379, 628, 465, 193, 526, 570, 133, 70, 340, 507, 785, 374, 350, 827, 213, 287, 404, 433, 31, 406, 167, 652, 459, 690, 364, 748, 437, 203, 347, 707, 745, 731, 135, 845, 714, 632, 300, 380, 622, 836, 476, 429, 489, 558, 290, 212, 8, 295, 108, 734, 571, 176, 524, 815, 248, 45, 159, 266, 651, 80, 738, 730, 268, 523, 666, 635, 267, 97, 408, 710, 249, 18, 840, 490, 166, 25, 475, 71, 275, 789, 568, 629, 169, 75, 756, 696, 305, 342, 787, 430, 546, 357, 68, 557, 276, 594, 175, 216, 337, 812, 701, 806, 725, 177, 202, 718, 3, 263, 431, 455, 446, 261, 251, 511, 482, 226, 24, 461, 432, 700, 200, 539, 15, 257, 14, 333, 229, 378, 663, 834, 376, 768, 517, 793, 99, 567, 797, 687, 646, 316, 792, 271, 57, 822, 604, 144, 802, 679, 158, 117, 399, 317, 88, 452, 753, 658, 382, 274, 6, 758, 4, 319, 40, 237, 210, 852, 211, 778, 715, 550, 464, 809, 303, 64, 595, 363, 311, 617, 265, 657, 98, 821, 673, 503, 338, 625, 277, 389, 103, 196, 576, 441, 752, 334, 162, 584, 583, 559, 231, 841, 134, 813, 341, 219, 814, 188, 192, 142, 410, 298, 472, 301, 692, 398, 614, 521, 128, 160, 356, 123, 805, 168, 847, 100, 496, 102, 105, 615, 654, 794, 235, 681, 683, 365, 795, 616, 803, 16, 682, 46, 512, 780, 344, 129, 269, 101, 440, 695, 348, 94, 468, 762, 742, 353, 293, 115, 1, 195, 613, 61, 332, 242, 582, 79, 35, 631, 43, 85, 289, 20, 574, 458, 205, 772, 206, 280, 538, 91, 425, 292, 93, 150, 674, 82, 87, 141, 256, 798, 339, 600, 39, 545, 766, 84, 230, 608, 826, 618, 314, 392, 451, 483, 172, 197, 722, 689, 449, 361, 201, 140, 312, 48, 368, 735, 96, 596, 241, 28, 232, 442, 751, 60, 12, 705, 829, 21, 779, 173, 38, 671, 469, 272, 349, 619, 69, 642, 245, 677, 329, 386, 817, 302, 703, 737, 130, 506, 346, 186, 355, 724, 438, 716, 137, 528, 323, 634, 453, 741, 415, 712, 204, 529, 849, 327, 532, 367, 400, 838, 41, 351, 199, 685, 721, 581, 223, 480, 837, 514, 369, 611, 182, 542, 185, 531, 132, 549, 234, 485, 672, 19, 407, 820, 560, 607, 403, 777, 450, 744, 116, 148, 556, 755, 246, 217, 111, 669, 37, 366, 118, 233, 759, 23, 258, 309, 602, 540, 377, 418, 547, 799, 207, 143, 81, 569, 773, 121, 454, 494, 26, 500, 396, 727, 516, 589, 774, 647, 318, 435, 218, 335, 732, 296, 667, 675, 791, 284, 22, 227, 2, 445, 548, 29, 498, 457, 5, 704, 281, 32, 421, 717, 627, 156, 833, 519, 790, 801, 586, 259, 297, 655, 502, 470, 553, 761, 10, 691, 7, 208, 660, 375, 598, 414, 291, 49, 686, 609, 448, 52, 308, 315, 488, 591, 391, 808, 501, 119, 848, 394, 831, 653, 527, 639, 86, 171, 27, 510, 662, 693, 491, 579, 736, 252, 552, 757, 131, 699, 626, 708, 565, 125, 9, 78, 543, 484, 767, 587, 54, 388, 670, 352, 487, 566, 250, 443, 165, 505, 264, 51, 107, 59, 478, 597, 796, 499, 181, 850, 466, 711, 749, 743, 198, 839, 279, 331, 786, 190, 534, 222, 114, 151, 460, 688, 187, 73, 729, 240, 145, 562, 255, 95, 610, 719, 371, 370, 515, 412, 493, 638, 800, 161, 426, 243, 680, 416, 343, 322, 561, 648, 30, 373, 851, 706, 56, 486, 509, 422, 713, 149, 533, 183, 0, 387, 564, 126, 294, 44, 676, 313, 823, 606, 109, 764, 58, 393, 818, 456, 599, 360, 709, 439, 174, 122]
        test_index4 = [810, 698, 63, 720, 782, 411, 723, 214, 573, 520, 694, 138, 383, 157, 643, 401, 66, 788, 697, 471, 770, 215, 771, 72, 320, 155, 238, 236, 359, 508, 253, 846, 358, 307, 286, 544, 504, 77, 191, 170, 405, 637, 152, 67, 577, 282, 825, 147, 605, 124, 110, 154, 551, 620, 593, 678, 636, 630, 541, 304, 649, 665, 247, 270, 424, 178, 354, 153, 481, 164, 819, 220, 306, 447, 228, 345, 321, 74, 843, 769, 104, 572, 225, 811, 146, 11, 397, 324, 640, 739, 385, 650, 824, 807, 419, 262, 92, 578, 844, 804, 36, 835, 260, 288, 784, 224, 832, 112, 409, 603, 728, 830, 283, 62, 513, 726, 209, 127, 590, 423, 13, 194, 776, 47, 65, 76, 477, 518, 645, 842, 536, 781, 34, 763, 362, 525, 17, 588, 816, 33, 592, 522, 239, 89, 580, 775, 740, 179, 326, 828, 42, 612, 299, 381, 497, 563, 656, 436, 120, 661, 106, 113, 221, 136, 537, 413, 330, 180, 641, 783, 384, 664, 479, 754, 90, 390, 684, 428, 535, 467, 633, 760, 474, 244, 53, 659, 554, 463, 555, 746, 189, 254, 50, 750, 434, 285, 83, 462, 372, 668, 495, 278, 427, 765, 420, 601, 585, 621, 624, 139, 417, 325, 184, 530]

        train_index3 = [487, 206, 843, 782, 115, 303, 535, 825, 19, 304, 107, 347, 530, 105, 842, 99, 317, 742, 459, 522, 723, 229, 109, 381, 702, 437, 713, 397, 610, 578, 238, 446, 314, 30, 691, 762, 682, 534, 233, 279, 606, 653, 729, 116, 68, 290, 556, 443, 567, 37, 594, 270, 106, 569, 251, 558, 354, 840, 215, 492, 717, 499, 169, 453, 53, 780, 743, 635, 151, 230, 661, 445, 593, 735, 188, 725, 669, 185, 43, 142, 552, 675, 621, 359, 806, 150, 67, 319, 427, 464, 697, 689, 350, 764, 432, 563, 706, 505, 131, 665, 296, 283, 711, 620, 130, 431, 322, 114, 477, 456, 428, 698, 271, 313, 512, 284, 129, 740, 389, 573, 210, 465, 523, 395, 424, 40, 306, 813, 204, 272, 8, 815, 70, 638, 790, 7, 710, 362, 709, 93, 491, 382, 79, 726, 342, 49, 250, 147, 814, 57, 442, 449, 407, 55, 440, 801, 450, 837, 472, 338, 419, 595, 25, 47, 174, 772, 59, 153, 518, 792, 161, 244, 707, 158, 411, 326, 832, 501, 498, 409, 639, 179, 651, 439, 736, 54, 654, 783, 168, 546, 615, 822, 417, 24, 298, 701, 671, 18, 667, 312, 254, 225, 87, 469, 528, 630, 222, 807, 570, 218, 680, 623, 490, 820, 529, 193, 831, 286, 66, 796, 71, 429, 412, 82, 775, 768, 703, 15, 781, 626, 514, 466, 406, 255, 584, 135, 683, 416, 29, 181, 227, 404, 364, 794, 104, 321, 268, 475, 828, 392, 542, 808, 241, 430, 574, 585, 203, 452, 757, 83, 118, 96, 467, 521, 166, 548, 189, 770, 705, 92, 366, 315, 261, 361, 138, 752, 276, 384, 56, 802, 829, 410, 88, 741, 582, 280, 756, 370, 139, 360, 460, 533, 287, 746, 539, 649, 202, 402, 340, 365, 23, 345, 800, 334, 310, 774, 353, 818, 240, 318, 633, 262, 98, 637, 769, 773, 89, 515, 331, 587, 433, 787, 624, 486, 550, 716, 850, 260, 305, 196, 140, 122, 494, 110, 84, 575, 513, 482, 589, 74, 821, 629, 273, 396, 154, 191, 788, 187, 50, 38, 418, 777, 208, 375, 463, 470, 517, 75, 248, 559, 302, 636, 817, 11, 485, 462, 835, 281, 253, 841, 617, 786, 577, 219, 425, 369, 687, 69, 580, 21, 77, 547, 849, 812, 125, 228, 42, 516, 572, 576, 798, 374, 205, 830, 6, 493, 809, 634, 259, 282, 590, 760, 833, 455, 320, 434, 299, 436, 696, 438, 325, 403, 265, 564, 602, 699, 278, 652, 553, 645, 799, 231, 245, 167, 502, 332, 426, 541, 162, 149, 226, 94, 221, 597, 473, 836, 601, 751, 34, 217, 72, 220, 213, 739, 394, 827, 367, 12, 753, 343, 198, 234, 420, 712, 608, 673, 297, 63, 607, 13, 435, 17, 708, 348, 207, 90, 307, 341, 380, 344, 471, 759, 551, 598, 32, 803, 657, 670, 172, 730, 791, 408, 846, 778, 200, 292, 583, 745, 510, 785, 724, 758, 834, 824, 489, 755, 750, 133, 60, 690, 26, 100, 531, 588, 852, 520, 363, 309, 604, 252, 544, 481, 441, 647, 476, 22, 62, 148, 483, 727, 776, 257, 52, 242, 173, 35, 178, 679, 738, 120, 275, 44, 300, 76, 720, 368, 212, 267, 311, 728, 444, 503, 495, 33, 9, 688, 160, 285, 295, 616, 625, 277, 779, 603, 484, 496, 182, 816, 684, 744, 36, 156, 2, 754, 508, 497, 308, 289, 560, 414, 421, 141, 223, 183, 804, 672, 511, 731, 611, 747, 117, 1, 113, 819, 686, 765, 165, 184, 677, 372, 274, 704, 0, 566, 540, 500, 718, 383, 405, 561, 20, 805, 176, 335, 379, 545, 171, 519, 507, 152, 618, 413, 609, 622, 581, 641, 316, 258, 662, 474, 337, 538, 504, 398, 423, 605, 660, 480, 422, 119, 650, 681, 714, 659, 789, 256, 643, 249, 664]
        test_index3 = [175, 851, 85, 674, 693, 91, 237, 86, 126, 666, 164, 247, 108, 10, 339, 536, 627, 386, 732, 844, 61, 448, 524, 591, 797, 692, 748, 685, 810, 640, 177, 28, 401, 562, 293, 571, 143, 48, 27, 246, 144, 121, 451, 838, 352, 695, 192, 506, 771, 461, 51, 65, 263, 378, 527, 216, 400, 694, 199, 376, 826, 614, 157, 385, 848, 333, 235, 568, 351, 145, 619, 648, 371, 722, 458, 349, 592, 80, 58, 599, 41, 766, 845, 468, 195, 45, 81, 103, 358, 613, 124, 586, 543, 288, 642, 291, 269, 214, 355, 391, 655, 763, 600, 847, 101, 330, 646, 373, 554, 737, 163, 612, 180, 324, 236, 73, 336, 415, 137, 700, 78, 155, 532, 579, 328, 102, 346, 46, 4, 123, 266, 839, 194, 390, 631, 793, 197, 357, 232, 111, 201, 16, 134, 327, 509, 676, 146, 387, 377, 663, 239, 658, 795, 632, 454, 393, 596, 128, 557, 767, 399, 668, 356, 525, 537, 734, 447, 39, 555, 31, 761, 209, 784, 644, 526, 112, 190, 132, 95, 224, 549, 823, 479, 3, 388, 733, 329, 5, 721, 656, 243, 628, 211, 159, 488, 97, 719, 264, 323, 749, 565, 294, 186, 127, 715, 457, 301, 64, 14, 678, 170, 811, 136, 478]

        train_index2 = [335, 706, 646, 791, 315, 108, 696, 802, 181, 230, 257, 804, 160, 371, 84, 747, 90, 513, 640, 309, 665, 393, 42, 776, 356, 552, 563, 157, 746, 321, 273, 656, 407, 387, 258, 111, 382, 453, 750, 452, 280, 694, 643, 291, 55, 669, 439, 340, 40, 838, 575, 286, 705, 178, 176, 691, 58, 338, 16, 310, 596, 763, 787, 473, 398, 384, 813, 542, 800, 29, 811, 295, 703, 826, 824, 203, 32, 377, 370, 156, 524, 397, 520, 751, 305, 3, 616, 130, 533, 712, 419, 591, 412, 376, 113, 48, 289, 594, 206, 330, 285, 634, 225, 518, 120, 402, 615, 221, 427, 171, 511, 653, 849, 423, 355, 704, 123, 333, 180, 161, 600, 784, 117, 818, 480, 573, 391, 737, 240, 134, 155, 139, 690, 60, 512, 165, 300, 443, 394, 297, 131, 314, 774, 627, 621, 464, 38, 249, 53, 194, 136, 378, 572, 281, 35, 521, 851, 476, 66, 470, 440, 623, 52, 608, 515, 815, 239, 246, 503, 28, 701, 265, 244, 103, 276, 110, 807, 159, 235, 597, 112, 463, 735, 532, 514, 329, 262, 223, 843, 728, 639, 535, 557, 167, 417, 241, 685, 475, 830, 24, 294, 731, 636, 715, 150, 41, 346, 94, 451, 217, 652, 381, 23, 268, 388, 352, 416, 292, 200, 173, 100, 489, 91, 642, 795, 709, 541, 502, 222, 214, 188, 354, 465, 822, 638, 353, 76, 242, 852, 73, 837, 556, 820, 425, 347, 118, 748, 114, 579, 581, 5, 667, 496, 505, 69, 14, 844, 526, 369, 78, 202, 154, 632, 553, 4, 571, 771, 54, 467, 266, 738, 293, 71, 559, 2, 25, 308, 216, 343, 740, 644, 166, 589, 839, 331, 177, 375, 437, 247, 373, 778, 472, 499, 543, 519, 832, 617, 658, 688, 307, 501, 234, 612, 430, 536, 191, 151, 435, 256, 654, 568, 662, 383, 145, 687, 752, 215, 719, 765, 567, 196, 718, 495, 17, 660, 27, 277, 395, 228, 320, 147, 806, 494, 449, 756, 106, 350, 523, 389, 448, 93, 259, 554, 754, 170, 254, 252, 306, 547, 829, 809, 428, 186, 269, 162, 413, 659, 672, 98, 6, 684, 726, 229, 264, 368, 593, 733, 744, 761, 403, 620, 189, 332, 303, 260, 144, 283, 727, 11, 695, 531, 469, 127, 624, 57, 33, 237, 782, 282, 586, 362, 243, 603, 92, 210, 337, 301, 85, 190, 39, 500, 507, 516, 104, 732, 233, 105, 341, 253, 408, 422, 208, 833, 739, 82, 497, 780, 583, 664, 87, 64, 270, 605, 274, 675, 770, 153, 613, 666, 410, 517, 44, 625, 390, 220, 140, 349, 357, 133, 261, 278, 79, 828, 115, 786, 713, 380, 792, 184, 673, 358, 36, 339, 753, 420, 149, 9, 45, 95, 767, 848, 548, 560, 298, 290, 415, 313, 421, 657, 122, 717, 698, 361, 336, 135, 724, 651, 367, 817, 769, 619, 8, 97, 825, 348, 509, 812, 21, 482, 821, 405, 840, 722, 478, 590, 491, 46, 364, 296, 49, 487, 224, 219, 801, 841, 647, 201, 562, 622, 845, 63, 604, 245, 442, 743, 574, 0, 539, 689, 187, 406, 148, 26, 461, 670, 655, 59, 714, 326, 424, 720, 477, 43, 661, 635, 528, 736, 483, 218, 741, 847, 783, 609, 485, 125, 768, 61, 81, 680, 324, 385, 846, 56, 19, 814, 86, 758, 649, 316, 34, 138, 766, 588, 498, 538, 555, 96, 83, 446, 474, 764, 366, 697, 585, 796, 760, 401, 759, 392, 797, 745, 271, 506, 850, 434, 648, 561, 207, 319, 834, 132, 50, 238, 564, 592, 450, 31, 121, 211, 351, 454, 302, 708, 88, 325, 323, 255, 570, 545, 550, 359, 51, 772, 102, 195, 679, 805, 628, 124, 404, 730, 287, 831, 47, 725, 587, 607, 433, 674, 263, 360, 75, 466, 299, 534, 584, 493, 527, 168]
        test_index2 = [650, 602, 250, 457, 447, 599, 549, 400, 248, 15, 618, 418, 479, 671, 631, 67, 37, 525, 819, 460, 372, 158, 65, 68, 799, 504, 128, 577, 484, 174, 444, 99, 192, 779, 205, 396, 197, 101, 777, 723, 379, 365, 510, 537, 342, 798, 345, 141, 582, 317, 546, 164, 558, 172, 227, 630, 183, 213, 456, 70, 363, 20, 175, 835, 808, 566, 595, 142, 374, 793, 700, 74, 432, 755, 288, 551, 414, 459, 318, 137, 334, 681, 678, 775, 762, 803, 7, 182, 606, 304, 199, 827, 445, 481, 226, 193, 742, 279, 468, 455, 327, 251, 411, 143, 312, 152, 522, 471, 789, 109, 816, 810, 438, 565, 710, 544, 179, 576, 540, 436, 284, 344, 429, 645, 823, 682, 614, 62, 18, 462, 530, 169, 633, 146, 22, 399, 490, 386, 668, 431, 729, 458, 107, 716, 629, 611, 601, 580, 89, 80, 794, 699, 212, 30, 10, 721, 693, 204, 409, 785, 77, 626, 1, 492, 198, 209, 711, 707, 578, 116, 232, 426, 322, 185, 311, 486, 637, 781, 119, 788, 663, 757, 13, 773, 231, 676, 441, 328, 749, 569, 129, 790, 842, 126, 529, 163, 686, 692, 598, 267, 275, 610, 641, 836, 677, 702, 72, 488, 272, 734, 236, 683, 12, 508]


        train_index1 = [783, 421, 598, 684, 501, 238, 681, 159, 428, 161, 518, 638, 399, 801, 525, 307, 13, 549, 679, 404, 430, 755, 92, 125, 114, 746, 415, 341, 76, 839, 819, 814, 189, 386, 132, 787, 837, 479, 349, 246, 255, 631, 40, 89, 429, 793, 68, 262, 139, 329, 118, 657, 789, 375, 445, 796, 453, 14, 82, 594, 529, 88, 273, 172, 434, 103, 639, 311, 45, 314, 541, 748, 613, 11, 214, 696, 147, 614, 700, 361, 676, 697, 578, 173, 305, 226, 31, 437, 803, 624, 285, 388, 781, 116, 841, 95, 363, 455, 345, 825, 459, 448, 62, 204, 761, 184, 91, 806, 426, 692, 29, 54, 674, 371, 576, 146, 221, 584, 766, 617, 449, 350, 165, 745, 80, 506, 310, 259, 323, 9, 579, 436, 671, 179, 27, 411, 720, 293, 443, 5, 197, 672, 670, 540, 261, 546, 122, 538, 38, 358, 733, 334, 666, 368, 162, 67, 124, 39, 4, 33, 403, 673, 335, 280, 592, 99, 622, 644, 236, 750, 528, 521, 464, 433, 641, 775, 537, 392, 352, 563, 507, 12, 186, 577, 844, 774, 374, 260, 484, 333, 153, 396, 587, 304, 200, 394, 815, 373, 800, 78, 312, 773, 794, 42, 446, 133, 516, 389, 573, 742, 555, 250, 601, 723, 527, 192, 220, 582, 636, 432, 603, 640, 30, 494, 581, 395, 157, 610, 272, 821, 512, 306, 747, 651, 102, 52, 156, 510, 402, 817, 97, 543, 128, 378, 177, 347, 110, 637, 379, 191, 419, 698, 343, 727, 142, 687, 6, 829, 267, 662, 237, 567, 531, 400, 383, 58, 689, 232, 784, 702, 442, 203, 602, 284, 98, 2, 836, 522, 487, 217, 360, 46, 820, 422, 225, 18, 168, 228, 292, 377, 517, 397, 227, 716, 643, 328, 283, 795, 658, 535, 93, 213, 337, 425, 682, 115, 158, 846, 112, 36, 105, 362, 365, 441, 351, 833, 249, 726, 677, 406, 729, 164, 843, 691, 708, 83, 649, 295, 70, 574, 790, 737, 553, 127, 717, 1, 558, 539, 308, 410, 171, 417, 680, 460, 739, 423, 315, 376, 524, 740, 438, 625, 150, 852, 556, 686, 409, 143, 526, 734, 705, 208, 440, 131, 380, 174, 533, 270, 407, 605, 123, 138, 51, 275, 826, 342, 256, 182, 300, 770, 240, 230, 326, 458, 465, 163, 167, 145, 206, 500, 188, 324, 724, 764, 575, 79, 688, 771, 721, 229, 725, 100, 290, 444, 810, 53, 391, 824, 851, 251, 499, 475, 271, 44, 113, 24, 211, 620, 169, 591, 830, 596, 520, 32, 611, 109, 136, 330, 222, 28, 287, 55, 827, 769, 48, 772, 835, 642, 545, 477, 547, 63, 413, 384, 759, 322, 451, 664, 234, 656, 557, 462, 424, 752, 303, 754, 219, 743, 296, 21, 420, 325, 199, 450, 137, 536, 646, 628, 212, 823, 799, 788, 505, 756, 231, 405, 568, 317, 183, 732, 730, 693, 609, 626, 485, 278, 630, 20, 170, 401, 791, 566, 176, 327, 706, 198, 470, 719, 694, 266, 615, 492, 130, 338, 758, 489, 572, 606, 193, 140, 416, 660, 476, 714, 152, 849, 10, 269, 96, 210, 842, 569, 548, 807, 532, 798, 332, 75, 712, 77, 263, 848, 149, 797, 514, 804, 469, 564, 461, 253, 369, 321, 695, 151, 813, 302, 190, 586, 348, 243, 87, 751, 655, 780, 418, 288, 648, 166, 595, 802, 155, 356, 381, 279, 126, 707, 777, 22, 616, 665, 282, 471, 738, 367, 25, 196, 64, 15, 466, 297, 621, 336, 26, 588, 43, 497, 792, 515, 818, 561, 454, 387, 71, 542, 456, 633, 431, 627, 653, 728, 264, 209, 316, 513, 313, 534, 319, 7, 393, 141, 86, 478, 503, 753, 215, 580, 562, 398, 668, 490, 252, 468, 357, 254, 276, 178, 281, 390, 508, 749, 583, 129, 144, 645, 715, 767, 72, 235, 37]
        test_index1 = [711, 247, 480, 467, 320, 647, 845, 268, 744, 552, 8, 699, 776, 632, 241, 710, 331, 493, 180, 84, 736, 205, 618, 223, 340, 498, 372, 840, 763, 741, 809, 760, 768, 509, 435, 496, 17, 355, 81, 265, 593, 486, 257, 117, 634, 675, 570, 73, 364, 473, 56, 585, 289, 757, 201, 488, 34, 778, 194, 94, 811, 294, 822, 274, 832, 382, 242, 90, 722, 47, 366, 612, 19, 101, 224, 65, 344, 812, 258, 828, 50, 286, 652, 60, 154, 704, 544, 589, 847, 600, 447, 685, 298, 452, 731, 301, 439, 523, 85, 599, 709, 346, 635, 187, 111, 504, 481, 597, 678, 604, 202, 650, 762, 805, 107, 782, 49, 427, 245, 181, 491, 121, 619, 59, 408, 663, 239, 3, 207, 16, 148, 559, 765, 607, 218, 659, 277, 779, 106, 23, 69, 309, 175, 244, 550, 565, 119, 608, 808, 370, 412, 248, 216, 120, 590, 701, 195, 551, 463, 530, 414, 623, 713, 61, 502, 831, 571, 786, 735, 654, 683, 135, 339, 318, 134, 834, 104, 185, 233, 57, 483, 519, 560, 785, 482, 667, 354, 690, 703, 816, 35, 495, 299, 472, 718, 41, 838, 474, 385, 629, 108, 554, 850, 661, 511, 0, 353, 359, 74, 160, 669, 66, 291, 457]



    else:

        #n = len(all_idx)
        #y_train, y_test = train_test_split(range(n), test_size=0.25, random_state=1)


        train_idx5 = [66, 83, 6, 72, 26, 55, 63, 68, 50, 21, 25, 33, 29, 39, 14, 59, 42, 69, 3, 43, 11, 74, 45, 79, 70, 85, 49, 91, 82, 19, 93, 38, 64, 2, 31, 81, 51, 71, 36, 46, 4, 0, 58, 5, 92, 1, 89, 41, 9, 18, 87, 47, 65, 75, 77, 44, 88, 86, 53, 15, 76, 7, 80, 30, 27, 62, 8, 73, 16, 61, 78]
        test_idx5 = [40, 37, 54, 48, 56, 20, 10, 60, 34, 28, 52, 32, 17, 22, 23, 24, 12, 84, 90, 94, 35, 13, 57, 67]
        train_index5 = list(itertools.chain.from_iterable([all_idx[i] for i in train_idx5]))
        test_index5 = list(itertools.chain.from_iterable([all_idx[i] for i in test_idx5]))
        random.shuffle(train_index5)

        train_idx4 = [5, 67, 19, 39, 29, 27, 4, 78, 61, 73, 18, 83, 7, 6, 43, 11, 75, 22, 68, 23, 12, 90, 25, 70, 48, 17, 31, 34, 15, 62, 81, 77, 28, 60, 64, 33, 45, 42, 51, 40, 32, 86, 49, 8, 30, 94, 66, 56, 79, 74, 21, 84, 0, 3, 52, 38, 44, 88, 36, 57, 85, 93, 58, 9, 50, 72, 87, 1, 69, 55, 46]
        test_idx4 = [80, 14, 13, 53, 59, 20, 37, 10, 63, 2, 16, 24, 35, 91, 47, 54, 26, 89, 71, 65, 76, 82, 41, 92]
        train_index4 = list(itertools.chain.from_iterable([all_idx[i] for i in train_idx4]))
        test_index4 = list(itertools.chain.from_iterable([all_idx[i] for i in test_idx4]))
        random.shuffle(train_index4)

        train_idx3 = [34, 17, 87, 81, 40, 5, 13, 31, 50, 11, 57, 46, 32, 83, 16, 27, 35, 36, 85, 92, 91, 64, 61, 76, 73, 18, 86, 54, 90, 28, 52, 79, 84, 49, 30, 82, 37, 48, 15, 59, 33, 43, 7, 62, 94, 29, 69, 51, 1, 60, 63, 2, 66, 22, 26, 14, 39, 44, 20, 38, 89, 10, 41, 74, 19, 21, 0, 72, 56, 3, 24]
        test_idx3 = [58, 23, 93, 9, 25, 6, 78, 68, 71, 47, 67, 65, 55, 70, 80, 45, 77, 88, 42, 53, 12, 8, 4, 75]
        train_index3 = list(itertools.chain.from_iterable([all_idx[i] for i in train_idx3]))
        test_index3 = list(itertools.chain.from_iterable([all_idx[i] for i in test_idx3]))
        random.shuffle(train_index3)

        train_idx2 = [5, 92, 56, 94, 89, 1, 18, 24, 44, 35, 60, 6, 48, 86, 10, 12, 74, 65, 90, 32, 19, 62, 71, 53, 9, 91, 17, 57, 55, 41, 61, 45, 64, 8, 70, 78, 85, 93, 26, 76, 50, 52, 81, 46, 68, 69, 77, 58, 33, 38, 51, 42, 4, 67, 39, 37, 20, 31, 63, 47, 88, 49, 34, 7, 75, 82, 43, 22, 72, 15, 40]
        test_idx2 = [36, 28, 54, 23, 16, 79, 2, 25, 83, 13, 59, 87, 84, 14, 0, 21, 3, 27, 73, 66, 11, 80, 30, 29]
        train_index2 = list(itertools.chain.from_iterable([all_idx[i] for i in train_idx2]))
        test_index2 = list(itertools.chain.from_iterable([all_idx[i] for i in test_idx2]))
        random.shuffle(train_index2)

        train_idx1 = [94, 35, 33, 48, 70, 66, 54, 36, 45, 52, 23, 34, 81, 56, 92, 15, 78, 41, 86, 26, 93, 43, 59, 4, 65, 21, 82, 3, 69, 30, 62, 42, 47, 51, 83, 24, 8, 17, 60, 0, 85, 57, 22, 61, 63, 7, 91, 13, 68, 80, 14, 29, 28, 11, 18, 20, 50, 25, 6, 71, 76, 1, 16, 64, 79, 5, 75, 9, 72, 12, 37]
        test_idx1 = [40, 31, 46, 58, 77, 49, 87, 44, 88, 90, 67, 27, 74, 84, 32, 55, 39, 10, 2, 38, 53, 73, 19, 89]
        train_index1 = list(itertools.chain.from_iterable([all_idx[i] for i in train_idx1]))
        test_index1 = list(itertools.chain.from_iterable([all_idx[i] for i in test_idx1]))
        random.shuffle(train_index1)

    cg_index = [501, 502, 503, 504, 505, 506, 507, 508, 509]
    if arch == "k40":
        for k in range(len(train_index1)):
            if train_index1[k] >= 510:
                train_index1[k] -= 9
        for k in range(len(train_index2)):
            if train_index2[k] >= 510:
                train_index2[k] -= 9
        for k in range(len(train_index3)):
            if train_index3[k] >= 510:
                train_index3[k] -= 9
        for k in range(len(train_index4)):
            if train_index4[k] >= 510:
                train_index4[k] -= 9
        for k in range(len(train_index5)):
            if train_index5[k] >= 510:
                train_index5[k] -= 9
        for k in range(len(test_index1)):
            if test_index1[k] >= 510:
                test_index1[k] -= 9
        for k in range(len(test_index2)):
            if test_index2[k] >= 510:
                test_index2[k] -= 9
        for k in range(len(test_index3)):
            if test_index3[k] >= 510:
                test_index3[k] -= 9
        for k in range(len(test_index4)):
            if test_index4[k] >= 510:
                test_index4[k] -= 9
        for k in range(len(test_index5)):
            if test_index5[k] >= 510:
                test_index5[k] -= 9



        for j in cg_index:
            if j in train_index1:
                train_index1.remove(j)
            if j in train_index2:
                train_index2.remove(j)
            if j in train_index3:
                train_index3.remove(j)
            if j in train_index4:
                train_index4.remove(j)
            if j in train_index5:
                train_index5.remove(j)

            if j in test_index1:
                test_index1.remove(j)
            if j in test_index2:
                test_index2.remove(j)
            if j in test_index3:
                test_index3.remove(j)
            if j in test_index4:
                test_index4.remove(j)
            if j in test_index5:
                test_index5.remove(j)

    if index_label == 1:
        return train_index1, test_index1
    elif index_label == 2:
        return train_index2, test_index2
    elif index_label == 3:
        return train_index3, test_index3
    elif index_label == 4:
        return train_index4, test_index4
    elif index_label == 5:
        return train_index5, test_index5


def rnnClassify100(data_group, y_label,  arch, model_eval):
    y_label = pd.Series(y_label)


    for index_label in range(1, 6):
        train_index, test_index = Index_split(index_label, model_eval)
        X_train = data_group[train_index]
        X_test = data_group[test_index]
        y_train = y_label[train_index]
        y_test = y_label[test_index]


        n_timesteps = 1800
        n_features = 4
        model = tf.keras.Sequential()
        model.add(layers.LSTM(256, input_shape=(n_timesteps, n_features)))
        model.add(layers.Dropout(0.4))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

        model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])


        checkpoint_path = "%s/resourceAll-100-%s-%s-%d.hdf5"%(arch,arch, model_eval, index_label)
        cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                     save_best_only=True,
                                                     monitor='val_loss',
                                                     mode='min')

        hist= model.fit(x=X_train,y=y_train,
                epochs=120,
                validation_split=0.25,
                callbacks = [cp_callback],
                batch_size = 256,
                class_weight={1:5, 0:1}
                 )

        df = pd.DataFrame.from_dict(hist.history)
        df.to_csv("%s/resourceAll-100-%s-%s-%d-history.csv"%(arch,arch, model_eval, index_label))

        model = tf.keras.models.load_model(checkpoint_path)
        loss, accuracy = model.evaluate(x=X_test, y=y_test)
        with open("%s/resourceAll-100-%s-%s-%d-testAccurcy.txt"%(arch,arch, model_eval, index_label), "w+") as f:
            f.write(str(accuracy))
            f.close()

        y_predict = model.predict_classes(data_group)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_label.index.tolist(), "predict":y_predict})
        df.to_csv("%s/resourceAll-100-%s-%s-%d-All.csv"%(arch,arch, model_eval, index_label))


        y_predict = model.predict_classes(X_test)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_test.index.tolist(), "predict":y_predict})
        df.to_csv("%s/resourceAll-100-%s-%s-%d-test.csv"%(arch,arch, model_eval, index_label))

def rnnClassify50(data_group, y_label,  arch, model_eval):
    y_label = pd.Series(y_label)


    for index_label in range(1, 6):
        train_index, test_index = Index_split(index_label, model_eval)
        X_train = data_group[train_index]
        X_test = data_group[test_index]
        y_train = y_label[train_index]
        y_test = y_label[test_index]


        n_timesteps = 3600
        n_features = 4
        model = tf.keras.Sequential()
        model.add(layers.LSTM(512, input_shape=(n_timesteps, n_features)))
        model.add(layers.Dropout(0.4))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

        model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])


        checkpoint_path = "%s/resourceAll-50-%s-%s-%d.hdf5"%(arch,arch, model_eval, index_label)
        cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                     save_best_only=True,
                                                     monitor='val_loss',
                                                     mode='min')

        hist= model.fit(x=X_train,y=y_train,
                epochs=120,
                validation_split=0.25,
                callbacks = [cp_callback],
                batch_size = 256,
                class_weight={1:5, 0:1}
                 )

        df = pd.DataFrame.from_dict(hist.history)
        df.to_csv("%s/resourceAll-50-%s-%s-%d-history.csv"%(arch,arch, model_eval, index_label))

        model = tf.keras.models.load_model(checkpoint_path)
        loss, accuracy = model.evaluate(x=X_test, y=y_test)
        with open("%s/resourceAll-50-%s-%s-%d-testAccurcy.txt"%(arch,arch, model_eval, index_label), "w+") as f:
            f.write(str(accuracy))
            f.close()

        y_predict = model.predict_classes(data_group)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_label.index.tolist(), "predict":y_predict})
        df.to_csv("%s/resourceAll-50-%s-%s-%d-All.csv"%(arch,arch, model_eval, index_label))


        y_predict = model.predict_classes(X_test)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_test.index.tolist(), "predict":y_predict})
        df.to_csv("%s/resourceAll-50-%s-%s-%d-test.csv"%(arch,arch, model_eval, index_label))


def rnnClassify10(data_group, y_label,  arch, model_eval):
    y_label = pd.Series(y_label)


    for index_label in range(1, 6):
        train_index, test_index = Index_split(index_label, model_eval)
        X_train = data_group[train_index]
        X_test = data_group[test_index]
        y_train = y_label[train_index]
        y_test = y_label[test_index]


        n_timesteps = 3600
        n_features = 4
        model = tf.keras.Sequential()
        model.add(layers.LSTM(512, input_shape=(n_timesteps, n_features)))
        model.add(layers.Dropout(0.4))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

        model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])


        checkpoint_path = "%s/resourceAll-10-%s-%s-%d.hdf5"%(arch,arch, model_eval, index_label)
        cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                     save_best_only=True,
                                                     monitor='val_loss',
                                                     mode='min')

        hist= model.fit(x=X_train,y=y_train,
                epochs=120,
                validation_split=0.25,
                callbacks = [cp_callback],
                batch_size = 256,
                class_weight={1:5, 0:1}
                 )

        df = pd.DataFrame.from_dict(hist.history)
        df.to_csv("%s/resourceAll-10-%s-%s-%d-history.csv"%(arch,arch, model_eval, index_label))

        model = tf.keras.models.load_model(checkpoint_path)
        loss, accuracy = model.evaluate(x=X_test, y=y_test)
        with open("%s/resourceAll-10-%s-%s-%d-testAccurcy.txt"%(arch,arch, model_eval, index_label), "w+") as f:
            f.write(str(accuracy))
            f.close()

        y_predict = model.predict_classes(data_group)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_label.index.tolist(), "predict":y_predict})
        df.to_csv("%s/resourceAll-10-%s-%s-%d-All.csv"%(arch,arch, model_eval, index_label))


        y_predict = model.predict_classes(X_test)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_test.index.tolist(), "predict":y_predict})
        df.to_csv("%s/resourceAll-10-%s-%s-%d-test.csv"%(arch,arch, model_eval, index_label))

def rnnClassifyOne(data_group, y_label, arch):
    #%%
    y_label = pd.Series(y_label)
    col_list = ["power", "memSize", "gpuU", "memU"]
    for i in [0, 1, 2, 3]:
        data_X = data_group[:, :, [i]]
        X_train, X_test, y_train, y_test = train_test_split(data_X, y_label, test_size=0.25, random_state=1)
        #X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)
        #print(X_train)
        X_train = np.asarray(X_train)
        X_test = np.asarray(X_test)
        n_timesteps = 1800
        n_features = 1
        model = tf.keras.Sequential()
        model.add(layers.LSTM(256, input_shape=(n_timesteps, n_features)))
        model.add(layers.Dropout(0.4))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

        model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

        fileM = col_list[i]
        checkpoint_path = "%s/%s-%s.hdf5"%(arch,fileM ,arch)
        cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                     save_best_only=True,
                                                     monitor='val_loss',
                                                     mode='min')

        hist= model.fit(x=X_train,y=y_train,
                epochs=120,
                validation_split=0.25,
                callbacks = [cp_callback],
                batch_size = 384,
                class_weight={1:8, 0:1}
                 )

        df = pd.DataFrame.from_dict(hist.history)
        df.to_csv("%s/%s-%s-history.csv"%(arch,fileM ,arch))


        loss, accuracy = model.evaluate(x=X_test, y=y_test)
        with open("%s/%s-%s-testAccurcy.txt"%(arch,fileM ,arch), "w+") as f:
            f.write(str(accuracy))
            f.close()

        y_predict = model.predict_classes(data_X)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_label.index.tolist(), "predict":y_predict})
        df.to_csv("%s/%s-%s-ALL.csv"%(arch,fileM ,arch))


        y_predict = model.predict_classes(X_test)
        y_predict = [ i[0] for i in y_predict.tolist()]
        df = pd.DataFrame.from_dict({"y_index":y_test.index.tolist(), "predict":y_predict})
        df.to_csv("%s/%s-%s-test.csv"%(arch,fileM ,arch))

def rnnClassifyTwo(data_group, y_label, arch):
    #%%
    y_label = pd.Series(y_label)
    col_list = ["power", "memSize", "gpuU", "memU"]
    for i in [0, 1, 2]:
        for j in range(i+1, 4):
            data_X = data_group[:, :, [i, j]]
            X_train, X_test, y_train, y_test = train_test_split(data_X, y_label, test_size=0.25, random_state=1)
            #X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)
            #print(X_train)
            X_train = np.asarray(X_train)
            X_test = np.asarray(X_test)
            n_timesteps = 1800
            n_features = 2
            model = tf.keras.Sequential()
            model.add(layers.LSTM(256, input_shape=(n_timesteps, n_features)))
            model.add(layers.Dropout(0.4))
            model.add(layers.Dense(128, activation='relu'))
            model.add(layers.Dense(16, activation='relu'))
            model.add(layers.Dense(1, activation='sigmoid'))

            model.compile(optimizer='adam',
                        loss='binary_crossentropy',
                        metrics=['accuracy'])

            fileM = col_list[i] + "-" + col_list[j]
            checkpoint_path = "%s/%s-%s.hdf5"%(arch,fileM ,arch)
            cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                         save_best_only=True,
                                                         monitor='val_loss',
                                                         mode='min')

            hist= model.fit(x=X_train,y=y_train,
                    epochs=120,
                    validation_split=0.25,
                    callbacks = [cp_callback],
                    batch_size = 384,
                    class_weight={1:8, 0:1}
                     )

            df = pd.DataFrame.from_dict(hist.history)
            df.to_csv("%s/%s-%s-history.csv"%(arch,fileM ,arch))


            loss, accuracy = model.evaluate(x=X_test, y=y_test)
            with open("%s/%s-%s-testAccurcy.txt"%(arch,fileM ,arch), "w+") as f:
                f.write(str(accuracy))
                f.close()

            y_predict = model.predict_classes(data_X)
            y_predict = [ i[0] for i in y_predict.tolist()]
            df = pd.DataFrame.from_dict({"y_index":y_label.index.tolist(), "predict":y_predict})
            df.to_csv("%s/%s-%s-ALL.csv"%(arch,fileM ,arch))


            y_predict = model.predict_classes(X_test)
            y_predict = [ i[0] for i in y_predict.tolist()]
            df = pd.DataFrame.from_dict({"y_index":y_test.index.tolist(), "predict":y_predict})
            df.to_csv("%s/%s-%s-test.csv"%(arch,fileM ,arch))

def rnnClassifyThree(data_group, y_label, arch):
    #%%
    y_label = pd.Series(y_label)
    col_list = ["power", "memSize", "gpuU", "memU"]
    for i in [0, 1]:
        for j in range(i+1, 3):
            for k in range(j+1, 4):
                data_X = data_group[:,:, [i, j, k]]
                X_train, X_test, y_train, y_test = train_test_split(data_X, y_label, test_size=0.25, random_state=1)
                #X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1)
                #print(X_train)
                X_train = np.asarray(X_train)
                X_test = np.asarray(X_test)
                n_timesteps = 1800
                n_features = 3
                model = tf.keras.Sequential()
                model.add(layers.LSTM(256, input_shape=(n_timesteps, n_features)))
                model.add(layers.Dropout(0.4))
                model.add(layers.Dense(128, activation='relu'))
                model.add(layers.Dense(16, activation='relu'))
                model.add(layers.Dense(1, activation='sigmoid'))

                model.compile(optimizer='adam',
                            loss='binary_crossentropy',
                            metrics=['accuracy'])

                fileM = col_list[i] + "-" + col_list[j]+ "-" + col_list[k]
                checkpoint_path = "%s/%s-%s.hdf5"%(arch,fileM ,arch)
                cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                             save_best_only=True,
                                                             monitor='val_loss',
                                                             mode='min')

                hist= model.fit(x=X_train,y=y_train,
                        epochs=120,
                        validation_split=0.25,
                        callbacks = [cp_callback],
                        batch_size = 384,
                        class_weight={1:8, 0:1}
                         )

                df = pd.DataFrame.from_dict(hist.history)
                df.to_csv("%s/%s-%s-history.csv"%(arch,fileM ,arch))

                model = tf.keras.models.load_model(checkpoint_path)
                loss, accuracy = model.evaluate(x=X_test, y=y_test)
                with open("%s/%s-%s-testAccurcy.txt"%(arch,fileM ,arch), "w+") as f:
                    f.write(str(accuracy))
                    f.close()

                y_predict = model.predict_classes(data_X)
                y_predict = [ i[0] for i in y_predict.tolist()]
                df = pd.DataFrame.from_dict({"y_index":y_label.index.tolist(), "predict":y_predict})
                df.to_csv("%s/%s-%s-ALL.csv"%(arch,fileM ,arch))


                y_predict = model.predict_classes(X_test)
                y_predict = [ i[0] for i in y_predict.tolist()]
                df = pd.DataFrame.from_dict({"y_index":y_test.index.tolist(), "predict":y_predict})
                df.to_csv("%s/%s-%s-test.csv"%(arch,fileM ,arch))



if __name__=="__main__":
    print("start loading")
    arch=sys.argv[1]
    sample_rate = 10
    data_group, y_label = load_group(arch, sample_rate)
    print("Done loading")
    model_eval = "seen"


    if sample_rate == 100:
        rnnClassify100(data_group, y_label,  arch, model_eval)
    elif sample_rate == 50:
        rnnClassify50(data_group, y_label,  arch, model_eval)
    elif sample_rate == 10:
        rnnClassify10(data_group, y_label,  arch, model_eval)
    #rnnClassifyOne(data_group, y_label, arch)
    #rnnClassifyTwo(data_group, y_label, arch)
    #rnnClassifyThree(data_group, y_label, arch)


