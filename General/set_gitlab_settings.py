#!/usr/bin/env python3
"""# **GitLab Repository Rules & Requirements**

This script automatically configures GitLab group and project settings according to
best practices for repository management.

## **How to Run**

Simply execute the script:

```bash
./set_gitlab_settings.py
```

## **Branch Protection**

- `master` and `development` branches are **protected**.
- **Direct pushes** to protected branches are **not allowed**.
- **Direct merges** into protected branches are **not allowed**.
- **Force push** is **disabled**.

## **Branch Naming Convention**

Only the following branch names are allowed:

- `master`
- `development`
- Branches that start with:
  - `feature/`
  - `hotfix/`
  - `bugfix/`

## **Merge Request (MR) Settings**

### **Defaults**

- Default branch: `master`
- Default merge method: **merge** (not squash or rebase)
- Default MR settings:
  - **Squash** enabled by default
  - **Delete source branch** enabled by default (except for protected branches, which cannot be deleted)
  - Default reviewers (through description tag): `REVIEWERS_GROUP_ID`

### **Merge Requirements (Protected Branches Only)**

- **Merging into protected branches (`master` and `development`) is only allowed if all conditions below are met:**
  - **Pipeline must succeed** before merging.
  - **No merge** allowed if the pipeline was skipped.
  - **Approval required** before merging:
    - At least **one approval** from `X_REVIEWERS_GROUP_ID`.
    - If a `CODEOWNERS` file exists, its approval rules **supersede** the `X_REVIEWERS_GROUP_ID` requirement.
    - **Author cannot approve** their own merge request.
  - **Approvals reset on new commit**.

## **Commit Messages & Templates**

- **Merge commit template**:
  `"Merge branch '%{source_branch}' into '%{target_branch}'"`
- **Squash commit template**:
  `"Squashed commit of the following changes:\n\n%{title}\n\n%{description}"`
- **Default message for apply**:
  `"Apply suggestion"`
"""

import sys

import requests

GITLAB_URL = ""
GITLAB_TOKEN = ""
GROUP_ID = ""
REVIEWERS_GROUP_ID = ""


def setup_gitlab_session() -> requests.Session:
    """Initialize requests session with GitLab authentication."""
    if not all([GITLAB_URL, GITLAB_TOKEN, GROUP_ID, REVIEWERS_GROUP_ID]):
        print(
            "Error: GITLAB_URL, GITLAB_TOKEN, GROUP_ID, and REVIEWERS_GROUP_ID variables must be set"
        )
        sys.exit(1)

    session = requests.Session()
    session.headers.update(
        {"PRIVATE-TOKEN": GITLAB_TOKEN, "Content-Type": "application/json"}
    )
    return session, GITLAB_URL, GROUP_ID, REVIEWERS_GROUP_ID


def set_group_settings(
    session: requests.Session, gitlab_url: str, group_id: str
) -> None:
    """Set group-level settings."""
    # Set default branch
    response = session.put(
        f"{gitlab_url}/api/v4/groups/{group_id}", json={"default_branch": "master"}
    )
    if response.status_code != 200:
        print(f"❌ Error setting default branch: {response.text}")
    else:
        print("✅ Default branch set to master")

    # Set push rules (branch naming convention)
    push_rules_data = {
        "branch_name_regex": "^(master|development|feature/.*|hotfix/.*|bugfix/.*)$"
    }

    # First try to update existing push rules
    response = session.put(
        f"{gitlab_url}/api/v4/groups/{group_id}/push_rule", json=push_rules_data
    )

    # If push rules don't exist (404), create them
    if response.status_code == 404:
        response = session.post(
            f"{gitlab_url}/api/v4/groups/{group_id}/push_rule", json=push_rules_data
        )

    if response.status_code not in [200, 201]:
        print(f"❌ Error setting push rules: {response.text}")
    else:
        print("✅ Push rules updated successfully")


def get_group_name(session: requests.Session, gitlab_url: str, group_id: str) -> str:
    """Get the full name of a GitLab group."""
    response = session.get(f"{gitlab_url}/api/v4/groups/{group_id}")
    if response.status_code != 200:
        print(f"❌ Error getting group name: {response.text}")
        return ""

    return response.json()["full_path"]


def set_project_settings(
    session: requests.Session, gitlab_url: str, group_id: str, reviewers_group_id: str
) -> None:
    """Set project-level settings for all projects in the group."""
    # Get all projects in the group
    response = session.get(f"{gitlab_url}/api/v4/groups/{group_id}/projects")
    if response.status_code != 200:
        print(f"❌ Error getting projects: {response.text}")
        return

    projects = response.json()
    print(f"\nFound {len(projects)} projects in group")

    # Project settings to apply
    project_settings = {
        # Merge request settings
        "merge_method": "merge",
        "squash_option": "default_on",  # Enable squash by default
        "remove_source_branch_after_merge": True,  # Enable delete source branch by default
        # Commit templates
        "merge_commit_template": "Merge branch '%{source_branch}' into '%{target_branch}'",
        "squash_commit_template": "Squashed commit of the following changes:\n\n%{title}\n\n%{description}",
        "suggestion_commit_message": "Apply suggestion",
        # automatically adding reviewers to merge requests (i.e. "default reviewers")
        "merge_requests_template": f"/assign_reviewer @{get_group_name(session, gitlab_url, reviewers_group_id)}\n",
        # Additional settings
        "printing_merge_request_link_enabled": True,
        # Pipeline requirements
        "only_allow_merge_if_pipeline_succeeds": True,
        "allow_merge_on_skipped_pipeline": False,
    }

    for project in projects:
        project_id = project["id"]
        project_name = project["name"]

        try:
            # Update project settings
            response = session.put(
                f"{gitlab_url}/api/v4/projects/{project_id}", json=project_settings
            )
            if response.status_code != 200:
                print(
                    f"❌ Error updating settings for project {project_name}: {response.text}"
                )
            else:
                print(f"✅ Project settings updated for {project_name}")

            # Set branch protection rules
            for branch in ["master", "development"]:
                # First try to delete existing protection
                try:
                    session.delete(
                        f"{gitlab_url}/api/v4/projects/{project_id}/protected_branches/{branch}"
                    )
                except:
                    pass

                # Create new protection rules
                protection_data = {
                    "name": branch,
                    "push_access_level": 0,  # No one can push
                    "merge_access_level": 30,  # Developers can merge approved MRs
                    "allow_force_push": False,  # Force push is disabled
                    "code_owner_approval_required": True,
                }

                response = session.post(
                    f"{gitlab_url}/api/v4/projects/{project_id}/protected_branches",
                    json=protection_data,
                )
                if response.status_code not in [200, 201]:
                    print(
                        f"❌ Error setting branch protection for {branch} in project {project_name}: {response.text}"
                    )
                else:
                    print(
                        f"✅ Branch protection set for {branch} in project {project_name}"
                    )

            # Create approval rule for all protected branches
            approval_rule = {
                "name": "Protected branches approval rule",
                "approvals_required": 1,
                "rule_type": "regular",
                "user_ids": [],
                "group_ids": [reviewers_group_id],
                "applies_to_all_protected_branches": True,
                "prevents_author_approval": True,
                "reset_approvals_on_push": True,
            }

            response = session.post(
                f"{gitlab_url}/api/v4/projects/{project_id}/approval_rules",
                json=approval_rule,
            )
            if response.status_code == 201:
                print(
                    f"✅ Approval rules set for protected branches in project {project_name}"
                )
            else:
                print(
                    f"❌ Error setting approval rules for project {project_name}: {response.json()}"
                )

        except Exception as e:
            print(f"❌ Error processing project {project_name}: {str(e)}")


def main():
    """Main function to set all GitLab settings."""
    session, gitlab_url, group_id, reviewers_group_id = setup_gitlab_session()

    print("Setting group-level settings...")
    set_group_settings(session, gitlab_url, group_id)

    print("\nSetting project-level settings...")
    set_project_settings(session, gitlab_url, group_id, reviewers_group_id)

    print("\nAll settings have been applied!")


if __name__ == "__main__":
    main()
