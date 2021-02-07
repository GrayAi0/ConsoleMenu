



# Dict Tools
import os


class Dict:

    @staticmethod
    def beshure(retdict: dict, shuredict: dict, typeshure = True):
        for sukey in shuredict:
            suvalue = shuredict[sukey]
            if isinstance(suvalue, dict):
                if not sukey in retdict or not isinstance(retdict[sukey], dict):
                    retdict[sukey] = shuredict[sukey]
                else:
                    retdict[sukey] = Dict.beshure(retdict[sukey], suvalue, typeshure)

                continue

            if not sukey in retdict or (typeshure and not isinstance(suvalue, type(retdict[sukey]) )):
                retdict[sukey] = suvalue


        return retdict

# str tools
class Str:

    @staticmethod
    def getLenof(chr: str, fstr: str) -> int:
        return len(fstr) - len(fstr.replace(chr, ''))

class System:

    @staticmethod
    def cls():
        os.system('cls')