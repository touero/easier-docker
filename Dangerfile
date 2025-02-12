modified_files = git.modified_files + git.added_files
deleted_files = git.deleted_files

total_lines_changed = git.lines_of_code

summary = "### 🤖 PR Auto Summary\n"
summary += "🚀 **Total affected files**: #{modified_files.count + deleted_files.count}\n"
summary += "🆕 **New files**: #{git.added_files.count}\n"
summary += "✏️ **Modified files**: #{git.modified_files.count}\n"
summary += "🗑️ **Deleted files**: #{git.deleted_files.count}\n"
summary += "📊 **Total lines changed**: #{total_lines_changed}\n"
summary += "📂 **Key modified files**:\n"

modified_files.first(5).each do |file|
  summary += "  - `#{file}`\n"
end

unless deleted_files.empty?
  summary += "🗂️ **Key deleted files**:\n"
  deleted_files.first(5).each do |file|
    summary += "  - `#{file}`\n"
  end
end

warn("PR description is empty. Please provide a detailed explanation of the changes.") if github.pr_body.nil? || github.pr_body.strip.empty?

source_branch = github.branch_for_head
target_branch = github.branch_for_base

warn("PR target branch is `#{target_branch}`. Ensure this PR follows the merge strategy!") if (target_branch == "main" || target_branch == "master") && !(source_branch == "dev" || source_branch == "develop")

warn("PR is marked as Work in Progress (WIP).") if github.pr_title.include? "WIP"

warn("Please add labels to this PR.") if github.pr_labels.empty?

markdown(summary)

python_files = (git.modified_files + git.added_files).select { |file| file.end_with?(".py") }

unless python_files.empty?
  flake8_result = `flake8 #{python_files.join(" ")}`
  flake8_exit_status = $?.exitstatus

  if flake8_exit_status != 0
    fail("Flake8 code issues found:\n```\n#{flake8_result}\n```")
  else
    message("No Flake8 issues found!")
  end
end
