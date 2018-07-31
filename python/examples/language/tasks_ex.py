# Tasks are a subclass of a Future and a wrapper around a coroutine.
# They give you the ability to keep track of when they finish processing.
# Because they are a type of Future, other coroutines can wait for a task and you can also
# grab the result of a task when it’s done processing.
import asyncio


async def my_task(seconds):
    """ A task to do for a number of seconds """
    print('This task is taking {} seconds to complete'.format(seconds))
    asyncio.sleep(seconds)
    return 'task finished'


if __name__ == '__main__':
    my_event_loop = asyncio.get_event_loop()
    try:
        print('task creation started')
        task_obj = my_event_loop.create_task(my_task(seconds=2))
        my_event_loop.run_until_complete(task_obj)
    finally:
        my_event_loop.close()

    print("The task's result was: {}".format(task_obj.result()))