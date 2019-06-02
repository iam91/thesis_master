package IQ;

import reference.Config;
import reference.Util;

import java.util.Arrays;
import java.util.List;

/**
 * Created by lz103 on 2017/5/1.
 */
public abstract class IncrementalQuantile {
    protected static final int M = Config.M;

    protected int N;
    protected int bufferXLength;
    protected long totalCount = 0; // 已经处理的数据个数
    protected double[] bufferData;
    protected double[] bufferQuantile;
    protected double[][] bufferX;
    protected double[][] bracketQ;
    protected static double[] probability = Config.probability;

    public IncrementalQuantile() {
        bracketQ = new double[M][4];
        bufferQuantile = new double[M];
    }

    public void update(List dataList) {
        fill(dataList);
        if (totalCount > 0) {
            CDFQ();
        }
        ECDF();
        computeBracketQ();
        refillQ();
    }

    protected abstract void fill(List<Double> dataList);

    protected void createBuffer(int newN) {
        if (totalCount == 0) {  //第一次计算
            N = newN;
            bufferXLength = N;
            bufferData = new double[N];
            bufferX = new double[bufferXLength][6];
        } else if (bufferXLength == N || N != newN) {   //第二次计算或最后一次计算
            N = newN;
            bufferXLength = M + N;
            bufferData = new double[N];
            bufferX = new double[bufferXLength][6];
        }
    }

    // 计算bufferX[1][]：CDF of Q
    protected void CDFQ() {
        for (int i = 0; i < bufferXLength; i++) {
            double x = bufferX[i][0];

            int count = Util.lessEqualCountOld(bufferQuantile, x);
            if (count == 0) {
                bufferX[i][1] = 0D;
            } else if (count == M) {
                bufferX[i][1] = 1D;
            } else {
                bufferX[i][1] = interpolate(x, count - 1);
            }
        }
//        for (int i = 0; i < bufferXLength; i++) {
//            double x = bufferX[i][0];
//            if (x < bufferQuantile[0]) {
//                bufferX[i][1] = 0D;
//            } else if (x >= bufferQuantile[M - 1]) {
//                bufferX[i][1] = 1D;
//            } else {
//                int index = rankPlus(x, bufferQuantile);
//                bufferX[i][1] = interpolate(x, index);
//            }
//        }
    }

    protected abstract double interpolate(double x, int m);

    protected double median(double x) {
        if (totalCount == 0) {
            return x;
        }
        if ((x >= (0.5 / totalCount)) && (x <= (1 - 0.5 / totalCount))) {
            return x;
        } else if (x < 0.5 / totalCount) {
            return (0.5 / totalCount);
        }
        return (1 - 0.5 / totalCount);
    }

    protected void ECDF() {
        Util.sort(bufferData);
        for (int i = 0; i < bufferXLength; i++) {
            double x = bufferX[i][0];
            int count = Util.lessCountOld(bufferData, x);
            bufferX[i][2] = (double) count / N;
            count = Util.lessEqualCountOld(bufferData, x);
            bufferX[i][3] = (double) count / N;
            bufferX[i][4] = (totalCount * bufferX[i][1] + N * bufferX[i][2]) / (totalCount + N);
            bufferX[i][5] = (totalCount * bufferX[i][1] + N * bufferX[i][3]) / (totalCount + N);
        }
    }

//    protected void ACDF() {
//        for (int i = 0; i < bufferXLength; i++) {
//
//        }
//    }

    protected void computeBracketQ() {
        Util.sort(bufferX, 4);
        for (int i = 0; i < M; i++) {
            int index = Util.lessCountOld(bufferX, 4, probability[i]);
            if (index > 0) index--;
            bracketQ[i][0] = bufferX[index][0];
            bracketQ[i][1] = bufferX[index][4];
        }
        Util.sort(bufferX, 5);
        for (int i = 0; i < M; i++) {
            int index = Util.lessEqualCountOld(bufferX, 5, probability[i]);
            if (index == bufferXLength) index--;
            bracketQ[i][2] = bufferX[index][0];
            bracketQ[i][3] = bufferX[index][5];
        }
    }

    protected abstract void refillQ();

    public abstract double[] getQuantile();

}
