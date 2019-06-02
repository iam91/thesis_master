package reference;

import java.text.DecimalFormat;
import java.util.Arrays;

/**
 * Created by LinZheng on 2017/9/10.
 */
public class GMMUtil {
    public double Threshold = 0.01;
    public int K;
    public double[] weightings;
    public double[] means;
    public double[] sigmas;
    public double TotalLoglikelihood = 0;
    public int NumOfEMIterations = 0;

    public static double minStart = Config.initMinStart;
    public static double maxEnd = Config.initMaxEnd;

    public int m = 10;
    public double[] datas;

    public static void main(String[] args) {
        System.out.println(log2(0.3625 * GaussianFunction(0, 4.2111, 0.234599766025)));
    }

    public GMMUtil(int k, double[] weighting, double[] mean, double[] sigma) {
        this.K = k;
        this.weightings = weighting;
        this.means = mean;
        this.sigmas = sigma;
    }

    public GMMUtil(int k) {
        this.K = k;
        this.weightings = new double[k];
        this.means = new double[k];
        this.sigmas = new double[k];
        for (int i = 0; i < k; i++) {
            weightings[i] = Config.weightings[i];
            means[i] = Config.means[i];
            sigmas[i] = Config.sigmas[i];
        }
    }

    public double pInverse(double y, double start, double end) {

        if (y < 1E-4) {
            return minStart;
        }

        double mid = (start + end) / 2;
        double midY = p(mid);

        while (Math.abs(midY - y) > 10E-6) {
            if (midY > y) {
                end = mid;
            } else {
                start = mid;
            }
            mid = (start + end) / 2;
            midY = p(mid);

        }
        return mid;
    }

    public double pInverse(double y) {

        if (y < 1E-4) {
            return minStart;
        }

        double start = minStart;
        double end = maxEnd;      //1-p(end)<10E-6即可，大概为13.1最小，但误差偏大
        double mid = (start + end) / 2;
        double midY = p(mid);

        while (Math.abs(midY - y) > 10E-6) {
            if (midY > y) {
                end = mid;
            } else {
                start = mid;
            }
            mid = (start + end) / 2;
            midY = p(mid);
        }
        return mid;
    }

    public double p(double x) {
        double y = 0;
        for (int i = 0; i < K; i++) {
            y += weightings[i] * Util.normalDistribution(means[i], sigmas[i], x);
        }
        return y;
    }

    public void initStartEnd() {
        while (p(minStart) > 10E-6) {
            minStart--;
        }
        while (p(maxEnd) < 1 - 10E-6) {
            maxEnd++;
        }
    }

    private void initData(double[] data) {
        datas = new double[m * data.length + 1];

        for (int i = 0; i < data.length-1; i++) {
            datas[i * m] = data[i];
            double x0 = p(data[i]);
            double x1 = p(data[i+1]);
            double x = x1 - x0;
            for (int j = 1; j < m; j++) {
                datas[i * m + j] = pInverse(x0 + j * x / m);
            }
        }
        datas[m * data.length] = data[data.length-1];
    }

    public int random() {
        int temp = 0;
        temp = (int) (Math.random() * 1000) + 1;
        return temp;
    }

    public static double log2(double num) {
        if (num == 0)
            return 0;
        else
            return (Math.log(num) / Math.log(2));
    }

    public static double GaussianFunction(double x_n, double mean, double sigma) {     // return N(x_n|...)
        double var = Math.pow(sigma, 2);
//        double var = sigma;

        double Prob = Math.pow(2 * Math.PI * var, -0.5) * Math.exp(-(Math.pow(x_n - mean, 2)) / (2 * var));
        return Prob;
    }

    public void model(double[] data) {
//        initData(data);
        datas = data;
        double ChangeInLogLikelihood = 1;

        double[] newWeightings = new double[K];
        double[] newMeans= new double[K];
        double[] newSigmas= new double[K];
        System.arraycopy(weightings, 0, newWeightings, 0, K);
        System.arraycopy(means, 0, newMeans, 0, K);
        System.arraycopy(sigmas, 0, newSigmas, 0, K);

        while (ChangeInLogLikelihood > Threshold) {
            double LogLikelihood = 0, ProbOfXn;
            // Total LogLikelihood...
            for (int i = 0; i < datas.length; i++) {
                ProbOfXn = 0;
                for (int j = 0; j < K; j++) {
                    ProbOfXn = ProbOfXn + newWeightings[j] * GaussianFunction(datas[i], newMeans[j], newSigmas[j]);
                }

                LogLikelihood = LogLikelihood + log2(ProbOfXn);
            }

            // E- Step   Calculating Responsibilities...

            double[][] Rspb = new double[datas.length][K];          // Tau_nk: n data points and k component mixture
            for (int i = 0; i < datas.length; i++) {
                ProbOfXn = 0;
                for (int j = 0; j < K; j++) {
                    Rspb[i][j] = newWeightings[j] * GaussianFunction(datas[i], newMeans[j], newSigmas[j]);
                    ProbOfXn = ProbOfXn + Rspb[i][j];
                }
                for (int j = 0; j < K; j++) {
                    Rspb[i][j] = Rspb[i][j] / ProbOfXn;
                }
            }

            // M-Step     Re-estimating Parameters...

            double[] N_k = new double[K];

            for (int k = 0; k < K; k++) {             // Calculating N_k's
                for (int n = 0; n < datas.length; n++) {
                    N_k[k] = N_k[k] + Rspb[n][k];
                }
            }

            // Calculating new means's
            for (int k = 0; k < K; k++) {
                newMeans[k] = 0;
                for (int n = 0; n < datas.length; n++) {
                    newMeans[k] = newMeans[k] + Rspb[n][k] * datas[n];
                }
                newMeans[k] = newMeans[k] / N_k[k];
            }

            // Calculating new sigmas's                 // Confusion...NOT SURE...in Norm Implementation...
            for (int k = 0; k < K; k++) {
                newSigmas[k] = 0;
                for (int n = 0; n < datas.length; n++) {
                    newSigmas[k] = newSigmas[k] + Rspb[n][k] * (datas[n] - newMeans[k]) * (datas[n] - newMeans[k]);
                }
                newSigmas[k] = Math.sqrt(newSigmas[k] / N_k[k]);
                if(newSigmas[k]==0){
                    return;
                }
            }

            // Calculating new weightings's
            for (int k = 0; k < K; k++) {
                newWeightings[k] = N_k[k] / datas.length;
            }

            double NewLogLikelihood = 0, ProbOfX = 0;

            // New Total LogLikelihood...
            for (int i = 0; i < datas.length; i++) {
                ProbOfX = 0;
                for (int j = 0; j < K; j++) {
                    ProbOfX = ProbOfX + newWeightings[j] * GaussianFunction(datas[i], newMeans[j], newSigmas[j]);
                }
                NewLogLikelihood = NewLogLikelihood + log2(ProbOfX);
            }

            // ChangeInTotalLogLikelihood
            ChangeInLogLikelihood = NewLogLikelihood - LogLikelihood;
            TotalLoglikelihood = NewLogLikelihood;
        }
        System.arraycopy(newWeightings, 0, weightings, 0, K);
        System.arraycopy(newMeans, 0, means, 0, K);
        System.arraycopy(newSigmas, 0, sigmas, 0, K);
    }

    public void print() {
        StringBuilder builder = new StringBuilder();
        DecimalFormat df = new DecimalFormat("#.#######");
        for (int j = 0; j < K; j++) {
            builder.append(weightings[j] + "\t");
            builder.append(means[j] + "\t");
            builder.append(sigmas[j] + "\n");
        }
        System.out.println(builder.toString());
    }


}
