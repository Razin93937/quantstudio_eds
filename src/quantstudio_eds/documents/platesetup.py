from lxml import etree

from quantstudio_eds.io import EDSZip

from ..models.plate import Plate, PlateKind
from ..models.well import Allele, Detector, DetectorTask, Marker, MarkerTask, SampleFeature, Well

NAME = "plate_setup"
PATHS = ["apldbio/sds/plate_setup.xml"]


def present(z: EDSZip) -> bool:
    return z.exists("apldbio/sds/plate_setup.xml")


def _parse_plate_kind(root: etree._Element) -> PlateKind:
    kwargs = {}
    for key, xml_tag in PlateKind.MAPPINGS.items():
        value = root.findtext(f".//PlateKind/{xml_tag}")
        if value:
            kwargs[key] = value
    return PlateKind(**kwargs)


def _parse_plate(root: etree._Element, plate_kind: PlateKind) -> Plate:
    kwargs = {}
    for key, xml_tag in Plate.MAPPINGS.items():
        value = root.findtext(f".//{xml_tag}")
        if value:
            if key in ["rows", "columns"]:
                kwargs[key] = int(value)
            else:
                kwargs[key] = value
    return Plate(plate_kind=plate_kind, **kwargs)


def _parse_wells(root: etree._Element, plate: Plate):
    for value in root.xpath(".//Wells/Well"):
        well_index = int(value.xpath(".//Index")[0].text)
        is_omit = value.xpath(".//IsOmit")[0].text.lower() == "true"
        well = Well(well_index, is_omit)
        plate.add_well(well)


def _parse_detector_tasks(root: etree._Element, plate: Plate):
    feature_map = root.xpath('.//FeatureMap/Feature/Name[text()="detector-task"]')
    if not feature_map:
        return
    parent = feature_map[0].getparent().getparent()
    for value in parent.xpath(".//FeatureValue"):
        well_index = int(value.xpath(".//Index")[0].text)
        for data in value.xpath(".//FeatureItem/DetectorTaskList/DetectorTask"):
            kwargs = {}
            for key, xml_tag in Detector.MAPPINGS.items():
                detector_elem = data.xpath(f".//Detector/{xml_tag}")
                if detector_elem:
                    kwargs[key] = detector_elem[0].text
            detector = Detector(**kwargs)
            task = data.xpath(".//Task")[0].text
            concentration = data.xpath(".//Concentration")[0].text
            detector_task = DetectorTask(detector=detector, task=task, concentration=concentration)
            plate.wells[well_index].add_detector_task(detector_task)


def _parse_sample_features(root: etree._Element, plate: Plate):
    feature_map = root.xpath('.//FeatureMap/Feature/Name[text()="sample"]')
    if not feature_map:
        return
    parent = feature_map[0].getparent().getparent()
    for value in parent.xpath(".//FeatureValue"):
        well_index = int(value.xpath(".//Index")[0].text)
        sample_elem = value.xpath(".//FeatureItem/Sample")[0]
        name = sample_elem.xpath(".//Name")[0].text
        color = sample_elem.xpath(".//Color")[0].text
        custom_property = sample_elem.xpath(".//CustomProperty")[0].text or ""
        sample = SampleFeature(name=name, color=color, custom_property=custom_property)
        plate.wells[well_index].add_sample_feature(sample)


def _parse_marker_tasks(root: etree._Element, plate: Plate):
    feature_map = root.xpath('.//FeatureMap/Feature/Name[text()="marker-task"]')
    if not feature_map:
        return
    parent = feature_map[0].getparent().getparent()
    for value in parent.xpath(".//FeatureValue"):
        well_index = int(value.xpath(".//Index")[0].text)
        for data in value.xpath(".//FeatureItem/MarkerTaskList/MarkerTask"):
            task = data.xpath(".//Task")[0].text
            marker_elem = data.xpath(".//Marker")[0]
            marker_kwargs = {}
            for key, xml_tag in Marker.MAPPINGS.items():
                elem = marker_elem.xpath(f".//{xml_tag}")
                if elem:
                    marker_kwargs[key] = elem[0].text
            alleles = []
            for allele_elem in marker_elem.xpath(".//*[starts-with(local-name(), 'Allele')]"):
                allele_kwargs = {}
                for key, xml_tag in Allele.MAPPINGS.items():
                    elem = allele_elem.xpath(f".//{xml_tag}")
                    if elem:
                        allele_kwargs[key] = elem[0].text
                alleles.append(Allele(**allele_kwargs))
            marker = Marker(alleles=alleles, **marker_kwargs)
            marker_task = MarkerTask(marker=marker, task=task)
            plate.wells[well_index].add_marker_task(marker_task)


def _parse_custom_properties(root: etree._Element, plate: Plate):
    # TODO: Implement parsing of custom properties if needed
    pass


def parse(z: EDSZip) -> dict:
    root = z.read_and_parse_xml(PATHS[0])
    plate_kind = _parse_plate_kind(root)
    plate = _parse_plate(root, plate_kind)
    _parse_wells(root, plate)
    _parse_detector_tasks(root, plate)
    _parse_sample_features(root, plate)
    _parse_marker_tasks(root, plate)
    _parse_custom_properties(root, plate)
    return plate
