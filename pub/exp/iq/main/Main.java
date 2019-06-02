package main;

import IQ.IQnonlinear;
import reference.Config;
import reference.Util;
import thread.barrier.MyBarrier;
import thread.consume.*;
import thread.produce.CSVProducer;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.concurrent.*;
import java.util.concurrent.atomic.DoubleAccumulator;


/**
 * Created by LinZheng on 2017/5/6.
 */
public class Main {

    private static int comsumerNum = 1;
    private static BlockingQueue blockingQueue = new LinkedBlockingDeque<>();
    private static CyclicBarrier barrier = new MyBarrier(comsumerNum, blockingQueue);

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        String path = "/Users/zwy/Documents/files/thesis/exp/data/";
        String eq = "result/eq.csv";
        String data = "data.csv";
        double[] EQ = Util.CSVReader(path + eq);
        initProducer(path + data);

        long t0 = System.currentTimeMillis();

        double[] result = testIQNew();
//        double[] result = testIQ();

        System.out.println(System.currentTimeMillis() - t0);
        System.out.println("-------------");
        for(double d: result) System.out.println(String.format("%15.6f", d));
        System.out.println("-------------");
        for(double d: Util.computeError(result, EQ)) System.out.println(String.format("%15.6f", d));
    }

    private static void initProducer(String fileName) {
        CSVProducer dataProducer = new CSVProducer(fileName, blockingQueue);
        Thread dataThread = new Thread(dataProducer);
        dataThread.start();
    }

    private static FutureTask getIQlinear() {
        FutureTask<double[]> iqlinearTask = new FutureTask(new IQlinearConsumer(blockingQueue, barrier));
        Thread iqlinearThread = new Thread(iqlinearTask);
        iqlinearThread.start();
        return iqlinearTask;
    }

    private static FutureTask getIQnonlinear() {
        FutureTask<double[]> iqnonlinearTask = new FutureTask(new IQnonlinearConsumer(blockingQueue, barrier));
        Thread iqnonlinearThread = new Thread(iqnonlinearTask);
        iqnonlinearThread.start();
        return iqnonlinearTask;
    }

    private static FutureTask getIQnonlinearNew() {
        FutureTask<double[]> iqnonlinearTask = new FutureTask(new IQnonlinearNewConsumer(blockingQueue, barrier));
        Thread iqnonlinearThread = new Thread(iqnonlinearTask);
        iqnonlinearThread.start();
        return iqnonlinearTask;
    }

    private static FutureTask getIQnonlinearAuto() {
        FutureTask<double[]> iqnonlinearTask = new FutureTask(new IQnonlinearAutoConsumer(blockingQueue, barrier));
        Thread iqnonlinearThread = new Thread(iqnonlinearTask);
        iqnonlinearThread.start();
        return iqnonlinearTask;
    }

    private static FutureTask getIQnonlinear(IQConsumer iqnonlinearConsumer) {
        FutureTask<double[]> iqnonlinearTask = new FutureTask(iqnonlinearConsumer);
        Thread iqnonlinearThread = new Thread(iqnonlinearTask);
        iqnonlinearThread.start();
        return iqnonlinearTask;
    }

    public static double[] testIQ() throws ExecutionException, InterruptedException {
        FutureTask<double[]> IQlinearTask = getIQlinear();
        return IQlinearTask.get();
    }

    public static double[] testIQNew() throws ExecutionException, InterruptedException {
        FutureTask<double[]> IQnonlinearTask = getIQnonlinear();
        return IQnonlinearTask.get();
    }

    public static double[] testIQAuto() throws ExecutionException, InterruptedException {
        FutureTask<double[]> IQnonlinearTask = getIQnonlinearAuto();
        return IQnonlinearTask.get();
    }

    public static void testMaxEnd() throws ExecutionException, InterruptedException {
        int date = 20150821;
        double[] EQ = Util.CSVReader(Config.inputPath + Config.dataType + "EQ/" + date + "_" + Config.M + "_EQ.csv");

        initProducer(date + ".csv");
        double[][] result = new double[comsumerNum][];
        long t0 = System.currentTimeMillis();

        FutureTask<double[]>[] tasks = new FutureTask[comsumerNum];
        tasks[0] = getIQlinear();

        IQnonlinear[] IQnonlinears = new IQnonlinear[comsumerNum - 1];

//        for (int i = 0; i < comsumerNum - 1; i++) {
//            IQnonlinears[i] = new IQnonlinear();
//            IQnonlinears[i].setMaxEnd(13.1 + 0.1 * i);
//            tasks[i + 1] = getIQnonlinear(new IQConsumer(blockingQueue, barrier, IQnonlinears[i]));
//        }

        double[][] error = new double[comsumerNum][];
        for (int i = 0; i < comsumerNum; i++) {
            result[i] = tasks[i].get();
            error[i] = Util.computeError(result[i], EQ);
            System.out.printf("%d %f %f\n", i, Util.computeExtremeError(error[i]), error[i][(int) (Config.M * 0.95)]);
        }

        System.out.println(System.currentTimeMillis() - t0);
    }

}
