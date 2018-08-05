typedef struct _task {
  int prio;
  int affinity;
} task;

typedef struct {
  short set_work_msecs;
  short set_sleep_msecs;
  int work_msecs;
  int sleep_msecs;
  int runtime;
  int task_num;
  struct _task *head;
} run_config;

void        print_config(run_config *config);
run_config* parse_config(const char *filename);
void        apply_task_config(task t);
