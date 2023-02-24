import portio
EC_IBF_BIT = 0b10
EC_OBF_BIT = 0b01
EC_CMD_STATUS_REGISTER_PORT = 0x66
EC_DATA_REGISTER_PORT = 0x62
EC_MAP = {}
def inb(port):
    return portio.inb(port)

def outb(port,data):
    return portio.outb(data,port)

res_sc = portio.ioperm(EC_CMD_STATUS_REGISTER_PORT,1,1)
res_data = portio.ioperm(EC_DATA_REGISTER_PORT,1,1)
if (res_sc != 0 or res_data !=0):
    raise Exception("ioperm error")


class EC:
    class Register():
        @staticmethod
        def WaitInputNFull():
            while EC.Register.GetStatus() & EC_IBF_BIT != 0:
                pass

        @staticmethod
        def WaitOutputFull():
            i = 0
            while EC.Register.GetStatus() & EC_OBF_BIT == 0:
                if i == 0xFFFF:
                    break
                i += 1

        @staticmethod
        def GetStatus():
            return inb(EC_CMD_STATUS_REGISTER_PORT)

        @staticmethod
        def SetCmd(cmd: int):
            EC.Register.WaitInputNFull()
            outb(EC_CMD_STATUS_REGISTER_PORT, cmd)

        @staticmethod
        def SetData(data: int):
            EC.Register.WaitInputNFull()
            outb(EC_DATA_REGISTER_PORT, data)

        @staticmethod
        def GetData():
            EC.Register.WaitOutputFull()
            return inb(EC_DATA_REGISTER_PORT)

    @staticmethod
    def Read(address: int):
        EC.Register.SetCmd(0x80)
        EC.Register.SetData(address)
        return EC.Register.GetData()

    @staticmethod
    def ReadLonger(address:int,length:int):
        sum=0
        for len in range(length):
            EC.Register.SetCmd(0x80)
            EC.Register.SetData(address+len)
            sum = (sum<<8) + EC.Register.GetData()
        return sum


    @staticmethod
    def Write(address:int,data:int):
        EC.Register.SetCmd(0x81)
        EC.Register.SetData(address)
        EC.Register.SetData(data)
    
    def PrintAll():
        print("","\t",end="")
        for z in range(0xf+1):
            print(hex(z),"\t",end="")
        print()
        for x in range(0xf+1):
            for y in range(0xf+1):
                if y==0x00:
                    print(hex(x),"\t",end="")
                EC_MAP[(x<<4)+y]=EC.Read((x<<4)+y)
                print(EC_MAP[(x<<4)+y],"\t",end="")
                #print(EC.Read((x<<4)+y),"\t",end="")
            print()

    def GetDif():
        global EC_MAP
        for x in range(0xf+1):
            for y in range(0xf+1):
                index=(x<<4)+y
                nowvalue=EC.Read(index)
                if not EC_MAP.get(index):
                    EC_MAP[index]=nowvalue
                if EC_MAP[index] != nowvalue:
                    print(f"address: {hex(index)} oldValue: {hex(EC_MAP[index])} newValue: {hex(nowvalue)}")
                    EC_MAP[index] = nowvalue
cnt=0
while(True):
    cnt=cnt+1
    print(f"count: {cnt}")
    EC.GetDif()
