from quantstudio_eds.documents.utils import get_jaxb_setting_value
from quantstudio_eds.io import EDSZip
from quantstudio_eds.models.plate import Plate
from quantstudio_eds.models.setting import Setting, SettingsGroup

NAME = "analysisprotocol"
PATHS = ["apldbio/sds/analysis_protocol.xml"]


def present(z):
    return z.exists(PATHS[0])


def parse(z: EDSZip, plate: Plate) -> Plate:
    root = z.read_and_parse_xml(PATHS[0])
    settings_list = []
    for value in root.xpath(".//JaxbAnalysisSettings"):
        setting_type = value.xpath(".//Type")[0].text.split(".")[-1]
        settings = []
        for setting in value.xpath(".//JaxbSettingValue"):
            key = setting.xpath(".//Name")[0].text
            val = get_jaxb_setting_value(setting)
            settings.append(Setting(name=key, value=val))
        settings_list.append(SettingsGroup(setting_type=setting_type, settings=settings))

    plate.set_analaysis_protocol(settings_list)
    return plate
