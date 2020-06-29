import converter
import argparse
import os
sep = os.sep


def run(input_path = 'input'+sep+'code.png', output_path= 'output', bg= False, gamma= False):
    """

    :param input_path:  input path to images/image
    :param output_path: output path to directory where to save images
    :param bg: background processing
    :param gamma: gamma technique
    :return: None
    """

    converter.run(input_path, output_path, bg,gamma)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', default='input'+sep+'code.png', type=str, help='Directory to input images or path to input image -- default: '
                                                                                             'input'+sep+'code.png')
    parser.add_argument('-o', '--output_path', default='output', type=str, help=' Path to output directory where generated code will be saved -- default: '
                                                                                'output')
    parser.add_argument('-b', '--bg', default=False, type=bool, help=' Employ background processing along with Neural LSTM engine. -- default: False')
    parser.add_argument('-g', '--gamma', default=False, type=bool, help=' Adjust input image gamma level -- default: False')
    args = parser.parse_args()
    run(args.input_path, args.output_path,args.bg, args.gamma)

if __name__ == '__main__':
    main()
