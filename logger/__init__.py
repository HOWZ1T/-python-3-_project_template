from injection import inject


@inject('definitions')
@inject('datetime')
@inject('inspect')
@inject('sys')
@inject('os')
class Console:
    __tag = "[ logger ]"

    def __init__(self, definitions, datetime, inspect, sys, os, verbose=False):
        self.definitions = definitions
        self.datetime = datetime
        self.inspect = inspect
        self.sys = sys
        self.os = os
        self._verbose = verbose
        self.__boot__()

    def __sys_print__(self, msg):
        cur_time = "[ " + self.datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S") + " ]"
        if self._verbose:
            self.sys.stdout.write(cur_time + " " + self.__tag + " " + msg + "\n")

    def __sys_err__(self, msg, critical=False):
        cur_time = "[ " + self.datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S") + " ]"
        if self._verbose and not critical:
            self.sys.stderr.write(cur_time + " " + self.__tag + " " + msg + "\n")
        elif critical:
            self.sys.stderr.write(cur_time + " " + self.__tag + " " + msg + "\n")

    def __boot__(self):
        success = 1
        self.__sys_print__("booting logger...")

        if not self.os.path.exists(self.definitions.INFO_LOG):
            self.__sys_print__("creating info log...")

            try:
                tmp_file = open(self.definitions.INFO_LOG, "w+")
                self.__sys_print__("info log created")
            except Exception as e:
                success = 0
                self.__sys_err__(e, True)
            finally:
                tmp_file.close()
                del tmp_file  # garbage collection

        if not self.os.path.exists(self.definitions.ERR_LOG):
            self.__sys_print__("creating error log...")

            try:
                tmp_file = open(self.definitions.ERR_LOG, "w+")
                self.__sys_print__("error log created")
            except Exception as e:
                success = 0
                self.__sys_err__(e, True)
            finally:
                tmp_file.close()
                del tmp_file  # garbage collection

        res = "unknown error occurred"
        if success == 1:
            res = "successfully booted"
        else:
            res = "failed to boot"

        self.__sys_print__(res)

    def log(self, msg, is_err=False, critical=False):
        cur_time = "[ " + self.datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S") + " ]"
        tag = ""

        try:
            module_name = self.inspect.stack()[1][1].split('/')
            module_name = module_name[len(module_name) - 1]
            tag = "[ " + module_name + " ] "
            if self.inspect.stack()[1][3] != "<module>":
                tag += "[ " + self.inspect.stack()[1][3] + " ] "
            else:
                tag += "[ module ] "
        except Exception as e:
            self.__sys_err__("could not get log caller details!")

        data = cur_time + " " + tag + msg + "\n"

        try:
            if is_err:
                if self._verbose or critical:
                    self.sys.stderr.write(data)

                with open(self.definitions.ERR_LOG, "a+") as elog:
                    elog.write(data)
            else:
                if self._verbose or critical:
                    self.sys.stdout.write(data)

                with open(self.definitions.INFO_LOG, "a+") as ilog:
                    ilog.write(data)
        except Exception as e:
            self.__sys_err__("could not log data! Exception:\n" + e)

    def clear_logs(self):
        try:
            self.os.remove(self.definitions.INFO_LOG)
            self.os.remove(self.definitions.ERR_LOG)
            self.__sys_print__("logs cleared. rebooting console...")
            self.__boot__()
        except Exception as e:
            self.__sys_err__(e, critical=True)


def fetch_console(verbose=False):
    return Console(verbose)
