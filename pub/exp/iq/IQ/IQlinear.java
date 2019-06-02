package IQ;

import java.util.Arrays;
import java.util.List;

/**
 * Created by LinZheng on 2017/5/4.
 */
public class IQlinear extends IncrementalQuantile {

    long sum = 0;

    public IQlinear() {
        super();
    }

    @Override
    protected void fill(List<Double> dataList) {
        createBuffer(dataList.size());
        for (int i = 0; i < N; i++) {
            bufferData[i] = dataList.get(i);
            bufferX[i][0] = bufferData[i];
            sum += bufferData[i];
        }
        if (bufferXLength > N) {
            for (int i = 0; i < M; i++) {
                bufferX[N + i][0] = bufferQuantile[i];
            }
        }
    }

    @Override
    protected double interpolate(double x, int m) {
        double x0 = bufferQuantile[m];
        double x1 = bufferQuantile[m + 1];
//        double p0 = probability[m];
//        double p1 = probability[m + 1];
        double p0 = median(probability[m]);
        double p1 = median(probability[m + 1]);
        double value = p0 + (p1 - p0) * (x - x0) / (x1 - x0);
        return value;
    }

    @Override
    protected void refillQ() {
        double p;
        for (int i = 0; i < M; i++) {
            if (bracketQ[i][0] == bracketQ[i][2] || bracketQ[i][1] == bracketQ[i][3]) {
                bufferQuantile[i] = bracketQ[i][0];
            } else {
                p = (bracketQ[i][3] - probability[i]) / (bracketQ[i][3] - bracketQ[i][1]);
                bufferQuantile[i] = p * bracketQ[i][0] + bracketQ[i][2] * (1 - p);
            }
        }
        totalCount = totalCount + N;
    }

    @Override
    public double[] getQuantile() {
        return bufferQuantile;
    }
}
