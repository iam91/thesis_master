package thread.barrier;

import java.util.concurrent.BlockingDeque;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CyclicBarrier;

/**
 * Created by LinZheng on 2017/5/10.
 */
public class MyBarrier extends CyclicBarrier {

    public MyBarrier(int parties, BlockingQueue blockingQueue) {
        super(parties, () -> {
            if (!blockingQueue.isEmpty()) blockingQueue.poll();
        });
    }
}
