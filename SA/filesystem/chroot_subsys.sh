# Create and manage a chrooted environment with overlay mount (using / as rootfs)
SUBSYS_DIR="./subsys"
ROOTFS="/"
CODE_DIR="./language"
WORK_DIR="./work"
BIND_DIR="./rootfs_bind"

create_overlay_dirs() {
    # Ensure required directories exist
    mkdir -p "$SUBSYS_DIR" "$WORK_DIR" "$BIND_DIR"
}

mount_overlay() {
    # Prepare temp bind mount directory

    # 1. Bind-mount ROOTFS into BIND_DIR
    sudo mount --bind "$(realpath "$ROOTFS")" "$(realpath "$BIND_DIR")"

    # # 2. use `mount --bind` to
    # sudo mkdir -p "$BIND_DIR/lang"
    # sudo mount --bind "$(realpath "$CODE_DIR")" "$(realpath "$BIND_DIR/lang")"
    # Bind will result affecting the original root filesystem

    # 2. Overlay: lowerdir=BIND_DIR, upperdir=CODE_DIR, workdir=WORK_DIR, merged at SUBSYS_DIR
    sudo mount -t overlay overlay \
        -o lowerdir="$(realpath "$BIND_DIR")",upperdir="$(realpath "$CODE_DIR")",workdir="$(realpath "$WORK_DIR")" \
        "$(realpath "$SUBSYS_DIR")"
}

run_in_chroot() {
    # Run given command (or bash) inside the chroot (here chroot "/" is just running command)
    if [ $# -eq 0 ]; then
        chroot "$SUBSYS_DIR" /bin/bash
    else
        chroot "$SUBSYS_DIR" "$@"
    fi
}

unmount_overlay() {
    # Unmount the overlay from /code
    umount "$SUBSYS_DIR"
}

# Example usage:
# create_overlay_dirs
# mount_overlay
# run_in_chroot /bin/bash
# unmount_overlay

# Note: Using / as rootfs means you are not isolating the filesystem—this is not a real chroot environment. All changes affect the real system.
#       Only /code will have the overlay effect. For true isolation, use a separate chroot rootfs.
$1 "${@:2}"
