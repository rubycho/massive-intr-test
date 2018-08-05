#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>
#include <sys/time.h>
#include <sys/resource.h>

#include "inih/ini.h"
#include "parser.h"

#define SECTION_MAX_LENGTH 20

#define SET_BIT(i, n) i |= 1UL << n;
#define CHECK_BIT(i, n) (i >> n) & 1U

static char *get_task_num(char *c) { strtok(c, "_"); return strtok(NULL, "_"); }
static int handler(void *user, const char *section,
  const char *name, const char *value) {
  run_config  *rconfig = (run_config *)user;
  char        section_bak[SECTION_MAX_LENGTH] = {0, };
  int         task_num;

  if (!strcpy(section_bak, section)) {
    fprintf(stderr, "[ERROR] unable to backup section string.\n");
    return 0;
  }

  // run_config section
  #define MATCH(s, n) strcmp(section, s) == 0 && strcmp(name, n) == 0
  if (MATCH("run_config", "runtime"))
    rconfig->runtime = atoi(value);
  if (MATCH("run_config", "task_num")) {
    rconfig->task_num = atoi(value);
    rconfig->head = (task *)calloc(rconfig->task_num, sizeof(task));
  }
  if (MATCH("run_config", "work_msecs")) {
    rconfig->work_msecs = atoi(value);
    rconfig->set_work_msecs = 1;
  }
  if (MATCH("run_config", "sleep_msecs")) {
    rconfig->sleep_msecs = atoi(value);
    rconfig->set_sleep_msecs = 1;
  }

  if (strncmp(section, "task", 4) != 0) return 1;

  // task section
  task_num = atoi(get_task_num(section_bak));
  if (task_num >= rconfig->task_num) {
    fprintf(stderr, "[ERROR] task_%d (max_task_num: %d)\n",
      task_num, rconfig->task_num);
    return 0;
  }

  #define T_MATCH(n) strcmp(name, n) == 0
  if (T_MATCH("affinity"))
    SET_BIT(rconfig->head[task_num].affinity, atoi(value));
  if (T_MATCH("prio"))
    rconfig->head[task_num].prio = atoi(value);

  return 1;
}

void print_config(run_config *config) {
  fprintf(stdout, "[RUN INFO]\n");
  fprintf(stdout, "WORK_MSECS = %d, SLEEP_MSECS = %d, # OF TASKS = %d, RUNTIME = %d\n",
    config->work_msecs, config->sleep_msecs, config->task_num, config->runtime);

  fprintf(stdout, "[TASKS]\n");
  for(int i=0; i<config->task_num; i++) {
    fprintf(stdout, "(TASK %3d) prio = %3d, affinity = ",
      i, config->head[i].prio);
    for(int j=31; j>=0; j--)
      fprintf(stdout, "%d", CHECK_BIT(config->head[i].affinity, j));
    fprintf(stdout, "\n");
  }
}

run_config* parse_config(const char *filename) {
  run_config* config = (run_config *)calloc(1, sizeof(run_config));

  if (ini_parse(filename, handler, config)) {
    fprintf(stderr, "[ERROR] Can't load the configuration file.\n");
    return NULL;
  }

  print_config(config);
  return config;
}

/* not a parser code, but let just place here */
void apply_task_config(task t) {
  cpu_set_t cpuset;
  CPU_ZERO(&cpuset);

  for(int i=0; i<32; i++)
    if (CHECK_BIT(t.affinity, i))
      CPU_SET(i, &cpuset);

  if (t.affinity) sched_setaffinity(getpid(), sizeof(cpu_set_t), &cpuset);
  setpriority(PRIO_PROCESS, getpid(), t.prio);
}
