package IQ;

import reference.Config;
import reference.GMMUtil;

import java.util.Arrays;
import java.util.List;

/**
 * Created by LinZheng on 2017/5/15.
 */
public class IQnonlinearOld extends IncrementalQuantile {

    //    protected static double minStart = 0;
//    protected static double maxEnd = 20;
    protected static double[] pInverseP = new double[M];

//    protected static double sum = 0;
//    protected static double sum_2 = 0;

    public static GMMUtil oGMM = new GMMUtil(Config.K);

    public IQnonlinearOld() {
        super();
        initPInverseP();
    }

    protected void initPInverseP() {
        oGMM.initStartEnd();
        for (int i = 0; i < M; i++) {
            pInverseP[i] = oGMM.pInverse(probability[i]);
        }
    }

    @Override
    protected void fill(List<Double> dataList) {
        createBuffer(dataList.size());
        for (int i = 0; i < N; i++) {
            double d = dataList.get(i);
            if (d > 0) {
                bufferData[i] = Math.log(dataList.get(i));
            }else{
                bufferData[i] = 0;
            }
//            sum += bufferData[i];
//            sum_2 += Math.pow(bufferData[i], 2);
            bufferX[i][0] = bufferData[i];
        }
        if (bufferXLength > N) {
            for (int i = 0; i < M; i++) {
                bufferX[N + i][0] = bufferQuantile[i];
            }
        }
    }

    @Override
    protected double interpolate(double x, int m) {
        return oGMM.p(pInverseP[m] + (pInverseP[m + 1] - pInverseP[m]) * (x - bufferQuantile[m]) / (bufferQuantile[m + 1] - bufferQuantile[m]));
//        double x0 = bufferQuantile[m];
//        double x1 = bufferQuantile[m + 1];
//        double tmp0 = pInverseP[m];
//        double tmp1 = pInverseP[m + 1];
//        double value = p(tmp0 + (tmp1 - tmp0) * (x - x0) / (x1 - x0));
////        if (value > maxEnd) System.out.printf("value: %f %f %f\n", value, tmp0, tmp1);
//        return value;
    }

    @Override
    protected void refillQ() {
        double tmp1, tmp3;
        double p;
        for (int i = 0; i < M; i++) {
            if (Math.abs(bracketQ[i][0] - bracketQ[i][2]) < 10e-6 || bracketQ[i][1] == bracketQ[i][3]) {
                bufferQuantile[i] = (bracketQ[i][0] + bracketQ[i][2]) / 2;
            } else if (Math.abs(probability[i] - bracketQ[i][3]) < 10e-6) {
                bufferQuantile[i] = bracketQ[i][2];
            } else if (Math.abs(probability[i] - bracketQ[i][1]) < 10e-6) {
                bufferQuantile[i] = bracketQ[i][0];
            } else {
                tmp1 = oGMM.pInverse(bracketQ[i][1], oGMM.minStart, pInverseP[i]);
                tmp3 = oGMM.pInverse(bracketQ[i][3], pInverseP[i], oGMM.maxEnd);

//                if(pInverseP[i]>tmp3){
//                    System.out.println(probability[i]+" "+bracketQ[i][3]+" "+pInverseP[i]+" "+tmp3);
//                }

                if (Math.abs(tmp1 - tmp3) < 10e-6) {
                    bufferQuantile[i] = (bracketQ[i][0] + bracketQ[i][2]) / 2;
                } else {
                    p = Math.abs(tmp3 - pInverseP[i]) / Math.abs(tmp3 - tmp1);

                    bufferQuantile[i] = p * bracketQ[i][0] + bracketQ[i][2] * (1 - p);
                    if (p > 1 || p < 0)
                        System.out.printf("refill:%f %f %f %f %f %f %f\n", p, tmp1, pInverseP[i], tmp3, bracketQ[i][1], bufferQuantile[i], bracketQ[i][3]);
                }
            }
        }
        totalCount = totalCount + N;
//        System.out.println(Arrays.toString(bufferQuantile));
//        System.out.println(totalCount);
    }

    @Override
    public double[] getQuantile() {
        double[] result = new double[M];
        for (int i = 0; i < M; i++) {
            result[i] = Math.exp(bufferQuantile[i]);
        }
        return result;
    }
}
