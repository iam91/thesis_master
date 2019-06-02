package reference;

import java.util.Arrays;

/**
 * Created by lz103 on 2017/5/1.
 */
public class Config {
    public static final int M = 101;    // bufferQuantile的默认大小
    public static final int N = 1000;    // bufferData的默认大小
    public static double[] probability;

    public static int m = 1;
    public static final int K = 7;
    public static double[] weightings;
    public static double[] means;
    public static double[] sigmas;
    public static double[] vars;

    public static double initMaxEnd = 43408384;
    public static double initMinStart = 0;


    //根据K初始化IQnonlinear中的相关参数
    static {
        switch (K) {
            case 1:
                weightings = new double[]{1};
                means = new double[]{5.1784};
                vars = new double[]{1.438};
                sigmas = new double[]{1.199166};
                break;
            case 2:
                break;
            case 3:
                weightings = new double[]{0.8766640950582397,0.0010752688330569315,0.12226063610871082};
                means = new double[]{10130.005847380298,38789631.49035656,470712.6002631635};
                vars = new double[]{147653341.8952936,21332887340672.0,399139140098.2212};
                break;
            case 4:
                weightings = new double[]{0.8766640950738007,0.0005376344086021517,0.12226063610898621,0.0005376344086021517};
                means = new double[]{10130.00584798369,34170879.999999925,470712.6008037941,43408383.9999999};
                vars = new double[]{147653341.91813824,2.500001,399139141897.77295,4.250001};
                break;
            case 5:
                weightings = new double[]{0.8694874550053431,0.0005376344086021517,0.12407106948929333,0.0005376344086021517,0.0053662066881657545};   //利用3日得到的5参数
                means = new double[]{9837.673767539412,43408383.9999999,363502.2868942396,34170879.999999925,2380896.5488965185};
                vars = new double[]{136811704.9689518,4.250001,195613634369.62692,2.500001,898474698697.6855};
                break;
            case 7:
                weightings = new double[]{0.6618596030128916,0.0005376344086021517,0.028242457974197433,0.0005376344086021517,0.004939708090702147,0.2631147551743932,0.040768206930612755};
                means = new double[]{4827.807427482991,34170879.999999925,1136176.7517234103,43408383.9999999,2454864.91814521,34890.12809644723,241365.9238514533};
                vars = new double[]{25270828.23608005,2.500001,44472142908.0791,4.250001,926199860100.2793,525653708.0350662,29046723829.797096};
                break;
        }
        if (sigmas == null) {
            sigmas = new double[K];
            for (int i = 0; i < K; i++) {
                sigmas[i] = Math.sqrt(vars[i]);
            }
        } else if (vars == null) {
            vars = new double[K];
            for (int i = 0; i < K; i++) {
                vars[i] = Math.pow(sigmas[i], 2);
            }
        }
    }

    static {
        probability = new double[M];
        for (int i = 0; i < M; i++) probability[i] = (double) i / (M - 1);
    }

    public static void showProbability() {
        System.out.println(Arrays.toString(probability));
    }

    public static String inputPath = "src/input/";
    public static String dataType = "delay/";

}
