package thread.consume;

//import old.IQ.IQlinear;
import IQ.IQlinear;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CyclicBarrier;

/**
 * Created by LinZheng on 2017/5/5.
 */
public class IQlinearConsumer extends IQConsumer {

    public IQlinearConsumer(BlockingQueue blockingQueue, CyclicBarrier cyclicBarrier) {
        super(blockingQueue, cyclicBarrier, new IQlinear());
    }
}
