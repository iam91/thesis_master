package thread.produce;

import reference.Config;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;

/**
 * Created by LinZheng on 2017/5/5.
 */
public class CSVProducer extends Thread {
    private int maxSize = Config.N;
    private List<Double> dataList;
    private String path;
    private BlockingQueue blockingQueue;

    public CSVProducer(String fileName, BlockingQueue blockingQueue) {
//        this.path = Config.inputPath + Config.dataType + fileName;
        this.path = fileName;
        this.blockingQueue = blockingQueue;
    }

    public void run() {
        String line;
        try {
            BufferedReader reader = new BufferedReader(new FileReader(path));
            int count = 0;
            while ((line = reader.readLine()) != null) {
                if (count == 0) {
                    dataList = new ArrayList(maxSize);
                }
                dataList.add(Double.parseDouble(line));
                count++;
                if (count == maxSize) {
                    blockingQueue.put(dataList);
                    count = 0;
                }
            }
            if (dataList.size() != maxSize) blockingQueue.put(dataList);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            try {
                blockingQueue.put(new ArrayList());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }

}
