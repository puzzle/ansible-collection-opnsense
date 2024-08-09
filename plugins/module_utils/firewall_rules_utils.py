#  Copyright: (c) 2024, Puzzle ITC, Fabio Bertagna <bertagna@puzzle.ch>
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
Utilities for firewall_rules module related operations.
"""
import dataclasses
from dataclasses import dataclass, asdict, field
from typing import List, Optional
from xml.etree.ElementTree import Element

from ansible_collections.puzzle.opnsense.plugins.module_utils import xml_utils
from ansible_collections.puzzle.opnsense.plugins.module_utils.config_utils import (
    OPNsenseModuleConfig,
)
from ansible_collections.puzzle.opnsense.plugins.module_utils.enum_utils import ListEnum


# pylint: disable=too-few-public-methods
class FirewallRuleAction(ListEnum):
    """Represents the rule filter policy."""

    PASS = "pass"
    BLOCK = "block"
    REJECT = "reject"


# pylint: disable=too-few-public-methods
class FirewallRuleDirection(ListEnum):
    """Represents the rule direction."""

    IN = "in"
    OUT = "out"


# pylint: disable=too-few-public-methods
class FirewallRuleProtocol(ListEnum):
    """Represents the protocol to filter in a rule."""

    ANY = "any"
    TCP = "tcp"
    UDP = "udp"
    TCP_UDP = "tcp/udp"
    ICMP = "icmp"
    ESP = "esp"
    AH = "ah"
    GRE = "gre"
    IGMP = "igmp"
    PIM = "pim"
    OSPF = "ospf"
    GGP = "ggp"
    IPENCAP = "ipencap"
    ST2 = "st2"
    CBT = "cbt"
    EGP = "egp"
    IGP = "igp"
    BBN_RCC = "bbn-rcc"
    NVP = "nvp"
    PUP = "pup"
    ARGUS = "argus"
    EMCON = "emcon"
    XNET = "xnet"
    CHAOS = "chaos"
    MUX = "mux"
    DCN = "dcn"
    HMP = "hmp"
    PRM = "prm"
    XNS_IDP = "xns-idp"
    TRUNK_1 = "trunk-1"
    TRUNK_2 = "trunk-2"
    LEAF_1 = "leaf-1"
    LEAF_2 = "leaf-2"
    RDP = "rdp"
    IRTP = "irtp"
    ISO_TP4 = "iso-tp4"
    NETBLT = "netblt"
    MFE_NSP = "mfe-nsp"
    MERIT_INP = "merit-inp"
    DCCP = "dccp"
    PC = "3pc"
    IDPR = "idpr"
    XTP = "xtp"
    DDP = "ddp"
    IDPR_CMTP = "idpr-cmtp"
    TP_PLUS_PLUS = "tp++"
    IL = "il"
    IPV6 = "ipv6"
    SDRP = "sdrp"
    IDRP = "idrp"
    RSVP = "rsvp"
    DSR = "dsr"
    BNA = "bna"
    I_NLSP = "i-nlsp"
    SWIPE = "swipe"
    NARP = "narp"
    MOBILE = "mobile"
    TLSP = "tlsp"
    SKIP = "skip"
    IPV6_ICMP = "ipv6-icmp"
    CFTP = "cftp"
    SAT_EXPAK = "sat-expak"
    KRYPTOLAN = "kryptolan"
    RVD = "rvd"
    IPPC = "ippc"
    SAT_MON = "sat-mon"
    VISA = "visa"
    IPCV = "ipcv"
    CPNX = "cpnx"
    CPHB = "cphb"
    WSN = "wsn"
    PVP = "pvp"
    BR_SAT_MON = "br-sat-mon"
    SUN_ND = "sun-nd"
    WB_MON = "wb-mon"
    WB_EXPAK = "wb-expak"
    ISO_IP = "iso-ip"
    VMTP = "vmtp"
    SECURE_VMTP = "secure-vmtp"
    VINES = "vines"
    TTP = "ttp"
    NSFNET_IGP = "nsfnet-igp"
    DGP = "dgp"
    TCF = "tcf"
    EIGRP = "eigrp"
    SPRITE_RPC = "sprite-rpc"
    LARP = "larp"
    MTP = "mtp"
    AX_25 = "ax.25"
    IPIP = "ipip"
    MICP = "micp"
    SCC_SP = "scc-sp"
    ETHERIP = "etherip"
    ENCAP = "encap"
    GMTP = "gmtp"
    IFMP = "ifmp"
    PNNI = "pnni"
    ARIS = "aris"
    SCPS = "scps"
    QNX = "qnx"
    A_N = "a/n"
    IPCOMP = "ipcomp"
    SNP = "snp"
    COMPAQ_PEER = "compaq-peer"
    IPX_IN_IP = "ipx-in-ip"
    CARP = "carp"
    PGM = "pgm"
    L2TP = "l2tp"
    DDX = "ddx"
    IATP = "iatp"
    STP = "stp"
    SRP = "srp"
    UTI = "uti"
    SMP = "smp"
    SM = "sm"
    PTP = "ptp"
    ISIS = "isis"
    CRTP = "crtp"
    CRUDP = "crudp"
    SPS = "sps"
    PIPE = "pipe"
    SCTP = "sctp"
    FC = "fc"
    RSVP_E2E_IGNORE = "rsvp-e2e-ignore"
    UDPLITE = "udplite"
    MPLS_IN_IP = "mpls-in-ip"
    MANET = "manet"
    HIP = "hip"
    SHIM6 = "shim6"
    WESP = "wesp"
    ROHC = "rohc"
    PFSYNC = "pfsync"
    DIVERT = "divert"


# pylint: disable=invalid-name,too-few-public-methods
class IPProtocol(ListEnum):
    """Represents the IPProtocol."""

    IPv4 = "inet"
    IPv6 = "inet6"
    IPv4_IPv6 = "inet46"


# pylint: disable=too-few-public-methods,fixme
class FirewallRuleStateType(ListEnum):
    """Represents the FirewallRuleStateType."""  # TODO not yet in the ansible parameters

    NONE = "none"
    KEEP_STATE = "keep state"
    SLOPPY_STATE = "sloppy state"
    MODULATE_STATE = "modulate state"
    SYNPROXY_STATE = "synproxy state"


@dataclass
class FirewallRuleTarget:
    """Used to represent a source or destination target for a firewall rule."""

    target: str
    address: str = "any"
    network: str = "any"
    port: str = "any"
    invert: bool = False

    @classmethod
    def from_ansible_params(cls, target: str, params: dict) -> "FirewallRuleTarget":
        """
        Class method to build a FirewallRuleTarget instance from ansible
        module parameters.
        :param target: Target name as in "source" or "destination".
        :param params: Ansible module parameters.
        :return: FirewallRuleTarget instance.
        """
        # if eg "source_ip" is "any" then we set the flag
        ansible_address: Optional[str] = params["address"]
        ansible_network: Optional[str] = params["network"]

        ansible_invert: bool = params["invert"]
        ansible_port: str = params["port"]

        return cls(
            target=target,
            address=ansible_address,
            network=ansible_network,
            port=ansible_port,
            invert=ansible_invert,
        )

    @classmethod
    def from_xml(cls, target: str, element: Element) -> "FirewallRuleTarget":
        """
        Class method to build a FirewallRuleTarget from a given ElementTree
        XML element.
        :param target: Target name as in "source" or "destination".
        :param element: The ElementTree element to parse from.
        :return: FirewallRuleTarget instance.
        """
        target_data: dict = xml_utils.etree_to_dict(element)[target]

        _any: bool = {"any": None} in target_data.values()

        address: str = "any" if _any else target_data.get("address", "any")
        network: str = "any" if _any else target_data.get("network", "any")
        invert: bool = "not" in target_data and target_data["not"] in ["1", None]
        return FirewallRuleTarget(
            target=target,
            address=address,
            network=network,
            port=target_data.get("port", "any"),
            invert=invert,
        )

    def as_etree_dict(self) -> dict:
        """
        Returns the instance in a dictionary serialized form ready
        for conversion to ElementTree elements.
        :return: serialized dictionary from instance.
        """
        data: dict = {}

        if self.invert:
            data["not"] = "1"

        for net_target in ["address", "network"]:
            if getattr(self, net_target) != "any":
                data[net_target] = getattr(self, net_target)

        if "address" not in data and "network" not in data:
            data["any"] = None

        if self.port != "any":
            data["port"] = self.port
        return data


# pylint: disable=too-many-instance-attributes, fixme
@dataclass
class FirewallRule:
    """Used to represent a firewall rule."""

    interface: str
    uuid: Optional[str] = None
    type: FirewallRuleAction = FirewallRuleAction.PASS
    descr: Optional[str] = None
    quick: bool = (
        True  # If the quick tag is not present, the tag is interpreted as true
    )
    ipprotocol: IPProtocol = IPProtocol.IPv4
    direction: Optional[FirewallRuleDirection] = None
    protocol: FirewallRuleProtocol = FirewallRuleProtocol.ANY
    source: FirewallRuleTarget = field(
        default_factory=lambda: FirewallRuleTarget("source")
    )
    destination: FirewallRuleTarget = field(
        default_factory=lambda: FirewallRuleTarget("destination")
    )
    disabled: bool = False
    log: bool = False
    category: Optional[str] = None

    extra_attributes: dict = field(default_factory=dict)

    def __post_init__(self):
        # Manually define the fields and their expected types
        enum_fields = {
            "type": FirewallRuleAction,
            "ipprotocol": IPProtocol,
            "protocol": FirewallRuleProtocol,
            "direction": FirewallRuleDirection,
        }

        for field_name, field_type in enum_fields.items():
            value = getattr(self, field_name)

            # Check if the value is a string and the field_type is a subclass of ListEnum
            if isinstance(value, str) and issubclass(field_type, ListEnum):
                # Convert string to ListEnum
                setattr(self, field_name, field_type.from_string(value))

    def to_etree(self) -> Element:
        """
        Converts the current FirewallRule object to an XML Element.

        This method takes the attributes of the FirewallRule object, represented as a dictionary,
        and constructs an XML Element structure. The method primarily focuses on converting
        attributes related to 'source' and 'destination' into nested XML tags.

        Attributes in the format "source_any", "destination_port", etc., are transformed into
        corresponding XML structures like `<source><any/></source>`. Boolean attributes are
        particularly handled to create empty tags if True (e.g., `<any/>`) or are omitted if False.
        Non-boolean attributes are converted into standard XML tags with values.

        The 'uuid' attribute of the object, if present, is added as an attribute to the XML element.
        Other unnecessary fields are removed during the conversion process.

        Returns:
        Element: An XML Element representing the FirewallRule object.

        Example:
        Given a FirewallRule object with attributes like {"source_any": "1", "source_port": 22},
        the output will be an XML element structured as:
        ```xml
        <rule>
            <source>
                <any/>
                <port>22</port>
            </source>
        </rule>
        ```

        Note: The method assumes the presence of a utility function `dict_to_etree` for
        converting dictionaries to XML elements.
        """
        rule_dict: dict = asdict(self)
        del rule_dict["uuid"]
        del rule_dict["extra_attributes"]

        for rule_key, rule_val in rule_dict.copy().items():
            if rule_key == "extra_attributes":
                continue
            if rule_key == "quick":
                if rule_val:
                    del rule_dict[rule_key]
                    continue
                rule_dict[rule_key] = "0"
            elif rule_key in ["source", "destination"]:
                rule_val.pop("target")
                rule_dict[rule_key] = getattr(self, rule_key).as_etree_dict()
            elif rule_val in [None, False]:
                del rule_dict[rule_key]
            elif issubclass(type(rule_val), ListEnum):
                rule_dict[rule_key] = rule_val.value
            elif isinstance(rule_val, bool):
                rule_dict[rule_key] = "1"

        for extra_key, extra_val in self.extra_attributes.items():
            rule_dict[extra_key] = extra_val

        element: Element = xml_utils.dict_to_etree("rule", rule_dict)[0]

        if self.uuid:
            element.attrib["uuid"] = self.uuid

        return element

    # pylint: disable=too-many-locals
    @classmethod
    def from_ansible_module_params(cls, params: dict) -> "FirewallRule":
        """
        Creates a FirewallRule object from Ansible module parameters.

        This class method constructs a FirewallRule object using parameters typically
        provided by an Ansible module. It extracts relevant information such as interface,
        action, description, and various source and destination attributes from the
        provided `params` dictionary.

        The method handles special cases such as the interpretation of 'any' values for
        source and destination IPs and the exclusion of null values in the final dictionary
        used to create the FirewallRule object.

        Parameters:
        params (dict): A dictionary containing Ansible module parameters. Expected keys include
        all module params documented in firewall_rules.py:DOCUMENTATION

        Returns:
        FirewallRule: An instance of FirewallRule initialized with the provided parameters.

        Example:
        ```python
        params = {
            "interface": "eth0",
            "action": "block",
            "source": {
                ...
            },
            "destination": {
                ...
            },
            # ... other parameters ...
        }
        rule = FirewallRule.from_ansible_module_params(params)
        ```
        """

        source_dict: dict = (
            params.get("source") if params.get("source") is not None else {}
        )
        destination_dict: dict = (
            params.get("destination", {})
            if params.get("destination") is not None
            else {}
        )
        rule_dict = {
            "interface": params.get("interface"),
            "type": params.get("action"),
            "descr": params.get("description"),
            "quick": params.get("quick"),
            "ipprotocol": params.get("ipprotocol"),
            "direction": params.get("direction"),
            "protocol": params.get("protocol"),
            "source": FirewallRuleTarget("source", **source_dict),
            "destination": FirewallRuleTarget("destination", **destination_dict),
            "log": params.get("log"),
            "category": params.get("category"),
            "disabled": params.get("disabled"),
        }

        rule_dict = {
            key: value for key, value in rule_dict.items() if value is not None
        }

        return cls(**rule_dict)

    @classmethod
    def from_xml(cls, element: Element) -> "FirewallRule":
        """
        Converts an XML element into a FirewallRule object.

        This static method transforms an XML element, expected to have 'rule' as its root, into a
        FirewallRule object. It handles elements such as 'source', 'destination', and their
        sub-elements like 'address', 'network', 'port', 'any', and 'not'.

        The method processes each direction ('source' or 'destination') and relevant keys.
        'any' and 'not' are converted to booleans, while other values are assigned as is.
        Elements not present are skipped. The 'uuid' attribute is also extracted from the XML.

        Changelog elements ('updated', 'created') are currently ignored.

        Parameters:
        element (Element): XML element with 'rule' as root.

        Returns:
        FirewallRule: Instance populated with data from the XML element.

        Example XML structure:
        ```xml
        <rule uuid="12345">
            <source>
                <any>1</any>
                <port>22</port>
                <address>192.168.1.1/24</address>
                <not>1</not>
            </source>
            <!-- ... other elements ... -->
        </rule>
        """

        rule_dict: dict = xml_utils.etree_to_dict(element)["rule"]

        rule_dict.update(
            disabled=rule_dict.get("disabled", "0") == "1",
            quick="quick" not in rule_dict,
            log=rule_dict.get("log", "0") == "1",
            uuid=element.attrib.get("uuid"),
        )

        rule_dict["source"] = FirewallRuleTarget.from_xml(
            "source", element.find("./source")
        )
        rule_dict["destination"] = FirewallRuleTarget.from_xml(
            "destination", element.find("./destination")
        )

        class_attribute_names: List[str] = list(
            map(lambda f: f.name, dataclasses.fields(cls))
        )

        rule_dict["extra_attributes"] = {}

        for k, v in rule_dict.copy().items():
            if k not in class_attribute_names:
                rule_dict["extra_attributes"][k] = v
                rule_dict.pop(k)

        return FirewallRule(**rule_dict)


class FirewallRuleSet(OPNsenseModuleConfig):
    """
    Manages a set of firewall rules in an OPNsense configuration.

    This class provides functionality to load, add, update, delete, and find firewall
    rules. It also checks for changes and saves the updated ruleset to the
    configuration file. The rules are represented as a list of `FirewallRule` objects.

    Attributes:
        _rules (List[FirewallRule]): List of firewall rules loaded from the configuration.

    Methods:
        __init__(self, path): Initializes the class with a given configuration file path.
        _load_rules(self): Loads firewall rules from the configuration file.
        changed(self): Returns True if the current rules differ from the loaded ones.
        add_or_update(self, rule): Adds a new rule or updates an existing one.
        delete(self, rule): Removes a specified rule from the ruleset.
        find(self, **kwargs): Finds a rule matching given criteria.
        save(self): Saves changes to the configuration file if there are any modifications.
    """

    _rules: List[FirewallRule]

    def __init__(self, path: str = "/conf/config.xml"):
        super().__init__(
            module_name="firewall_rules",
            config_context_names=["firewall_rules"],
            path=path,
        )
        self._rules = self._load_rules()

    def _load_rules(self) -> List[FirewallRule]:
        # /opnsense/filter Element containing a list of <rule>
        element_tree_rules: Element = self.get("rules")

        return [FirewallRule.from_xml(element) for element in element_tree_rules]

    @property
    def changed(self) -> bool:
        """
        Checks if the current set of firewall rules has changed compared to the
        loaded configuration.

        This property compares the current set of `FirewallRule` objects in `_rules`
        with the set loaded from the configuration file. It returns True if there are
        differences, indicating that changes have been made to the ruleset which are
        not yet saved to the configuration file.

        Returns:
            bool: True if the ruleset has changed, False otherwise.
        """
        return self._load_rules() != self._rules

    def add_or_update(self, rule: FirewallRule) -> None:
        """
        Adds a new firewall rule to the ruleset or updates an existing one.

        This method checks if the provided `rule` already exists in the ruleset. If it
        does, the existing rule is updated with the properties of the provided `rule`.
        If it does not exist, the new rule is appended to the ruleset. The comparison
        to check if a rule exists is based on the equality condition defined in the
        `FirewallRule` class.

        Parameters:
            rule (FirewallRule): The firewall rule to be added or updated in the ruleset.

        Returns:
            None: This method does not return anything.
        """

        existing_rule: Optional[FirewallRule] = next(
            (r for r in self._rules if r == rule), None
        )
        if existing_rule:
            existing_rule.__dict__.update(rule.__dict__)
        else:
            self._rules.append(rule)

    def delete(self, rule: FirewallRule) -> bool:
        """
        Removes a specified firewall rule from the ruleset.

        This method iterates through the current set of firewall rules and removes the rule
        that matches the provided `rule` parameter. The comparison for removal is based on
        the inequality of the `FirewallRule` objects. If the rule is not found, no action is taken.

        Parameters:
            rule (FirewallRule): The firewall rule to be removed from the ruleset.

        Returns:
            bool: True if rule was deleted, False if rule was already not present
        """

        if rule in self._rules:
            self._rules.remove(rule)
            return True
        return False

    def find(self, **kwargs) -> Optional[FirewallRule]:
        """
        Searches for a firewall rule that matches the given criteria.

        This method iterates through the ruleset and returns the first `FirewallRule` object
        that matches all the provided keyword arguments. The comparison is made by checking
        if each attribute of the rule (specified as a keyword argument) equals the corresponding
        value in `kwargs`. If no matching rule is found, the method returns None.

        Keyword Arguments:
            kwargs: Arbitrary keyword arguments used for searching. Each keyword argument
                    should correspond to an attribute of the `FirewallRule` class.

        Returns:
            Optional[FirewallRule]: The first matching rule object, or None if no match is found.
        """

        for rule in self._rules:
            match = all(
                getattr(rule, key, None) == value for key, value in kwargs.items()
            )
            if match:
                return rule
        return None

    def save(self) -> bool:
        """
        Saves the current set of firewall rules to the configuration file.

        This method first checks if there have been any changes to the ruleset using the `changed`
        property. If there are no changes, it returns False. Otherwise, it updates the configuration
        XML tree with the current set of rules and writes the updated configuration to the file.
        It then reloads the configuration from the file to ensure synchronization.

        The saving process involves removing the existing rules from the configuration XML tree,
        clearing the filter element, and then extending it with the updated set of rules
        converted to XML elements.

        Returns:
            bool: True if changes were saved, False if there were no changes to save.
        """

        if not self.changed:
            return False

        filter_element: Element = self._config_xml_tree.find(
            self._config_maps[self._module_name]["rules"]
        )

        self._config_xml_tree.remove(filter_element)
        filter_element.clear()
        filter_element.extend([rule.to_etree() for rule in self._rules])
        self._config_xml_tree.append(filter_element)
        return super().save(override_changed=True)
