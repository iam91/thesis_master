package reference;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;

/**
 * Created by LinZheng on 2017/5/2.
 */
public class Util {
    public static int lessEqualCountOld(double[] array, double target) {
        int result = 0;
        for (int i = 0; i < array.length; i++) {
            if (array[i] <= target) {
                result++;
            } else {
                break;
            }
        }
        return result;
    }

    public static int lessEqualCountOld(double[][] array, int k, double target) {
        int result = 0;
        for (int i = 0; i < array.length; i++) {
            if (array[i][k] <= target) {
                result++;
            } else {
                break;
            }
        }
        return result;
    }


    //利用二分查找求array中小于或等于target的元素个数。
    public static int lessEqualCount(double[] array, double target) {
        int start = 0;
        int end = array.length;
        //二分查找大于target的第一个元素的索引
        while (start < end) {
            int mid = start + ((end - start) >> 1);
            if (array[mid] <= target) {
                start = mid + 1;
            } else {
                end = mid;
            }
        }
        return start;

    }

    public static int lessCountOld(double[] array, double target) {
        int result = 0;
        for (int i = 0; i < array.length; i++) {
            if (array[i] < target) {
                result++;
            } else {
                break;
            }
        }
        return result;
    }

    public static int lessCountOld(double[][] array, int k, double target) {
        int result = 0;
        for (int i = 0; i < array.length; i++) {
            if (array[i][k] < target) {
                result++;
            } else {
                break;
            }
        }
        return result;
    }

    //利用二分查找求array中小于target的元素个数。
    public static int lessCount(double[] array, double target) {
        int start = 0;
        int end = array.length;
        //二分查找大于或等于target的第一个元素的索引
        while (start < end) {
            int mid = start + ((end - start) >> 1);
            if (array[mid] < target) {
                start = mid + 1;
            } else {
                end = mid;
            }
        }
        return start;
    }

    //利用二分查找求array中小于或等于target的元素个数。
    public static int lessEqualCount(double[][] array, int k, double target) {
        int start = 0;
        int end = array.length;
        //二分查找大于target的第一个元素的索引
        while (start < end) {
            int mid = start + ((end - start) >> 1);
            if (array[mid][k] < target) {
                start = mid + 1;
            } else {
                end = mid;
            }
        }
        return start;
    }

    //利用二分查找求array中小于target的元素个数。
    public static int lessCount(double[][] array, int k, double target) {
        int start = 0;
        int end = array.length;
        //二分查找大于或等于target的第一个元素的索引
        while (start < end) {
            int mid = start + ((end - start) >> 1);
            if (array[mid][k] <= target) {
                start = mid + 1;
            } else {
                end = mid;
            }
        }
        return start;
    }


    /*利用二分查找返回大小为2的int数组，其中：
    result[0]：array中小于target的元素个数；
    result[1]：array中小于或等于target的元素个数。
     */
    public static int[] binarySearch(double[] array, double target) {
        int[] result = new int[2];
        //二分查找大于或等于target的第一个元素的索引，即result[0]。
        int start = 0;
        int end = array.length;
        while (start < end) {
            int mid = start + ((end - start) >> 1);
            if (array[mid] < target) {
                start = mid + 1;
            } else {
                end = mid;
            }
        }
        result[0] = start;
        if (start == array.length || array[start] != target) {
            result[1] = start;
            return result;
        }
        //二分查找大于target的第一个元素的索引，即result[0]。
        start = result[0];
        end = array.length;
        while (start < end) {
            int mid = start + ((end - start) >> 1);
            if (array[mid] <= target) {
                start = mid + 1;
            } else {
                end = mid;
            }
        }
        result[1] = start;
        return result;
    }

    public static void sort(double[][] array, int k) {
        Arrays.sort(array, (o1, o2) -> {
            if (o1[k] == o2[k]) {
                return 0;
            }
            return o1[k] > o2[k] ? 1 : -1;
        });
    }

    public static void quickSort(double[][] a, int k) {
        int length = a[0].length;
        double tmp = 0D;
        for (int i = 0; i < length; i++) {
            for (int j = i + 1; j < length; j++) {
                if (a[k][i] > a[k][j]) {
                    for (double[] a1 : a) {
                        tmp = a1[i];
                        a1[i] = a1[j];
                        a1[j] = tmp;
                    }
                }
            }
        }
    }

    // 对数组进行排序
    public static void sort(double[] array) {
        Arrays.sort(array);
    }


    public static double[] CSVReader(String path) {
        String line;
        List<Double> dataList = new ArrayList<>();
        BufferedReader reader;
        try {
            reader = new BufferedReader(new FileReader(path));
            while ((line = reader.readLine()) != null) {
                dataList.add(Double.parseDouble(line));
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        int size = dataList.size();
        double[] result = new double[size];
        for (int i = 0; i < size; i++) {
            result[i] = dataList.get(i);
        }
        return result;
    }

    public static void CSVWriter(String path, double[] array) {
        File writeToFile = new File(path);
        try {
            writeToFile.createNewFile();
            BufferedWriter out = new BufferedWriter(new FileWriter(writeToFile));
            for (int i = 0; i < array.length; i++) {
                out.write(array[i] + "\r\n");
            }
            out.flush();
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void CSVWriter(String path, double[][] array) throws IOException {
        File writename = new File(path);
        writename.createNewFile();
        BufferedWriter out = new BufferedWriter(new FileWriter(writename));
        for (int i = 0; i < array[0].length; i++) {
            for (int j = 0; j < array.length - 1; j++) {
                out.write(Double.toString(array[j][i]) + ",");
            }
            out.write(Double.toString(array[array.length - 1][i]) + "\r\n");
        }
        out.flush();
        out.close();
    }

    public static void computeEQ(double[] probability, String name, boolean isSorted) {
        String path;
        int M = probability.length;
        double[] data;
        if (isSorted == false) {
            path = Config.inputPath + Config.dataType + name + "_" + M + ".csv";
            data = CSVReader(path);
            Arrays.sort(data);
        } else {
            path = Config.inputPath + Config.dataType + "sorted/" + name + "_sorted.csv";
            data = CSVReader(path);
        }
        int T = data.length;
        double[] EQ = new double[M];
        for (int i = 0; i < M; i++) {
            double p = probability[i];
            double px = p * (T - 1);
            int j = (int) java.lang.Math.floor(px);
            double g = px - j;
            if (g == 0) {
                EQ[i] = data[j];
            } else {
                EQ[i] = (1 - g) * data[j] + g * data[j + 1];
            }
        }
        String EQpath = Config.inputPath + Config.dataType + "EQ/" + name + "_" + M + "_EQ.csv";
        CSVWriter(EQpath, EQ);
    }

    public static double normalDistribution(double mean, double sigma, double x) {   //此处sigma为标准差
        double xTemp = (x - mean) / sigma;
        double value = standardNormalDistribution(xTemp);
        return value;
    }

    public static double standardNormalDistribution(double a) {
        double p = 0.2316419;
        double b1 = 0.31938153;
        double b2 = -0.356563782;
        double b3 = 1.781477937;
        double b4 = -1.821255978;
        double b5 = 1.330274429;

        double x = Math.abs(a);
        double t = 1 / (1 + p * x);

        double val = 1 - (1 / (Math.sqrt(2 * Math.PI)) * Math.exp(-1 * Math.pow(a, 2) / 2)) * (b1 * t + b2 * Math.pow(t, 2) + b3 * Math.pow(t, 3) + b4 * Math.pow(t, 4) + b5 * Math.pow(t, 5));

        if (a < 0) {
            val = 1 - val;
        }
        return val;
    }

    public static double[] computeError(double[] IQ, double[] EQ) {
        int M = Config.M;
        double[] error = new double[M];
        for (int i = 0; i < M; i++) {
            error[i] = Math.abs(IQ[i] - EQ[i]) / EQ[i];
//            System.out.printf("%.3f %f\n", (double) i / (M - 1), error[i] * 100);
        }
        return error;
    }

    public static double[][] computeError(double[][] IQ, double[] EQ) {
        int M = Config.M;
        double[][] error = new double[IQ.length][M];
        for (int i = 0; i < IQ.length; i++) {
            for (int j = 0; j < M; j++) {
                error[i][j] = Math.abs(IQ[i][j] - EQ[j]) / EQ[j];
            }
        }
        return error;
    }

    public static double computeExtremeError(double[] error) {
        double result = 0;
        int M = Config.M;
        for (int i = (M - 1) * 8 / 10; i < M; i++) {
            result += error[i];
        }
        return result;
    }

    public static void main(String[] args) {
        int M = 101;
        String name = "SD1";
        double[] probability = new double[M];
        for (int i = 0; i < M; i++) probability[i] = (double) i / (M - 1);
        computeEQ(probability,name,true);
    }


}
