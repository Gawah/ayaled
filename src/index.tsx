import {
  definePlugin,
  PanelSection,
  PanelSectionRow,
  ServerAPI,
  staticClasses,
  ToggleField
} from "decky-frontend-lib";
import { VFC,useState,useEffect } from "react";
import { FaLightbulb } from "react-icons/fa";
import { Backend } from "./backend";
import { Setting } from "./settings";
import { SlowSliderField } from "./SlowSliderField";

const Content: VFC = () => {
  const [ledOn, setledOn] = useState<boolean>(Setting.getLedOn());
  const [currentTargetRed, setCurrentTargetRed] = useState<number>(Setting.getRed());
  const [currentTargetGreen, setCurrentTargetGreen] = useState<number>(Setting.getGreen());
  const [currentTargetBlue, setCurrentTargetBlue] = useState<number>(Setting.getBlue());

  useEffect(() => {
    if(ledOn){
      Setting.setLedOn(currentTargetRed,currentTargetGreen,currentTargetBlue)
    }else{
      Setting.setOff()
    }
  }, [ledOn]);
  useEffect(() => {
    Setting.setRed(currentTargetRed);
    Setting.setGreen(currentTargetGreen);
    Setting.setBlue(currentTargetBlue);
  }, [currentTargetRed, currentTargetGreen, currentTargetBlue]);

  return (
    <PanelSection title="设置">
      <PanelSectionRow>
        <ToggleField
          label={"开启灯效"}
          checked={ledOn}
          onChange={(value) => {
            setledOn(value);
          }}
        />
      </PanelSectionRow>
      {ledOn&&<PanelSectionRow>
        <SlowSliderField
          label="Red"
          description={`Control red`}
          value={currentTargetRed}
          step={1}
          max={255}
          min={0}
          showValue={true}
          onChangeEnd={(value: number) => {
            setCurrentTargetRed(value);
          }}
        />
      </PanelSectionRow>}
      {ledOn&&<PanelSectionRow>
        <SlowSliderField
          label="Green"
          description={`Control green`}
          value={currentTargetGreen}
          step={1}
          max={255}
          min={0}
          showValue={true}
          onChangeEnd={(value: number) => {
            setCurrentTargetGreen(value);
          }}
        />
      </PanelSectionRow>}
      {ledOn&&<PanelSectionRow>
        <SlowSliderField
          label="Blue"
          description={`Control blue`}
          value={currentTargetBlue}
          step={1}
          max={255}
          min={0}
          showValue={true}
          onChangeEnd={(value: number) => {
            setCurrentTargetBlue(value);
          }}
        />
      </PanelSectionRow>}
    </PanelSection>
  );
};



export default definePlugin((serverApi: ServerAPI) => {
  Setting.loadSettingsFromLocalStorage();
  Backend.init(serverApi);
  Backend.applySettings();
  return {
    title: <div className={staticClasses.Title}>ayaled</div>,
    content: <Content/>,
    icon: <FaLightbulb/>,
    onDismount() {
      
    },
  };
});
