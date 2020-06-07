#define _GNU_SOURCE

#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sched.h>
#include <limits.h>

int
main (int argc, char **argv)
{
    int mountns, netns;

    char cwd_s[PATH_MAX];
    int cwd = 0;

    if (argc < 2) {
        fprintf(stderr, "No executable is specified.\n");
        return 1;
    }

    // Save current working directory
    if (getcwd(cwd_s, sizeof(cwd_s)) == NULL) {
        fprintf(stderr, "Failed to get current directory.\n");
    } else {
        cwd = open(cwd_s, O_DIRECTORY);
        if (cwd == -1) {
            perror("Failed to open current directory");
        }
    }

    // Enter the mount namespace
    mountns = open("/var/run/netns/confmountns/vpn", O_RDONLY);
    if (mountns == -1) {
        perror("Failed to open mount namespace reference");
        if (cwd > 0) { close(cwd); }
        return 1;
    }
    if (setns(mountns, CLONE_NEWNS) == -1) {
        perror("Failed to enter mount namespace");
        close(mountns);
        if (cwd > 0) { close(cwd); }
        return 1;
    }
    if (close(mountns) == -1) {
        perror("Failed to close mount namespace reference");
        if (cwd > 0) { close(cwd); }
        return 1;
    }

    // Restore current working directory
    if (cwd > 0) {
        if (fchdir(cwd) < 0) {
            perror("Failed to restore current directory");
        }
        if (close(cwd) == -1) {
            perror("Failed to close old current directory");
            return 1;
        }
    }

    // Enter the network namespace
    netns = open("/var/run/netns/vpn", O_RDONLY);
    if (netns == -1) {
        perror("Failed to open network namespace");
        return 1;
    }
    if (setns(netns, CLONE_NEWNET) == -1) {
        perror("Failed to enter network namespace");
        close(netns);
        return 1;
    }
    if (close(netns) == -1) {
        perror("Failed to close network namespace reference");
        return 1;
    }

    uid_t uid = getuid();
    if (uid != 0) {
        // Drop elevated priviliges
        if (setuid(uid) != 0) {
            perror("Failed to drop elevated priviliges");
            return 1;
        }
        if (setuid(0) != -1) {
            // Privileges can be restored, this is an error
            fprintf( stderr,
                "Failed to properly drop elevated priviges.\n" );
            return 1;
        }
    }

    // Execute the target process
    execvp(argv[1], argv + 1);
    perror("Failed to execute the target process");
    return 1;
}

