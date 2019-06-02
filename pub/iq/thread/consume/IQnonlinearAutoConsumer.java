package thread.consume;

import IQ.IQnonlinearAuto;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CyclicBarrier;

/**
 * Created by LinZheng on 2017/5/9.
 */
public class IQnonlinearAutoConsumer extends IQConsumer {
    public IQnonlinearAutoConsumer(BlockingQueue blockingQueue, CyclicBarrier cyclicBarrier) {
        super(blockingQueue, cyclicBarrier, new IQnonlinearAuto());
    }
}
