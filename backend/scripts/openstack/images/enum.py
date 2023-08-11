from enum import Enum


class ContainerFormat(Enum):
    ami: str = "ami"
    ari: str = "ari"
    aki: str = "aki"
    bare: str = "bare"
    ovf: str = "ovf"
    ova: str = "ova"
    docker: str = "docker"


class DiskFormat(Enum):
    ami: str = "ami"
    ari: str = "ari"
    aki: str = "aki"
    vhd: str = "vhd"
    vhdx: str = "vhdx"
    vmdk: str = "vmdk"
    raw: str = "raw"
    qcow2: str = "qcow2"
    vdi: str = "vdi"
    ploop: str = "ploop"
    iso: str = "iso"


class Status(Enum):
    queued: str = "queued"
    saving: str = "saving"
    active: str = "active"
    killed: str = "killed"
    deleted: str = "deleted"
    pending_delete: str = "pending_delete"
    deactivated: str = "deactivated"
    uploading: str = "uploading"
    importing: str = "importing"


class Visibility(Enum):
    public: str = "public"
    community: str = "community"
    shared: str = "shared"
    private: str = "private"
