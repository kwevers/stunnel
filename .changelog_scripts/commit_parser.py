# Source: https://python-semantic-release.readthedocs.io/en/latest/commit_parsing.html#custom-parsers
import git
import semantic_release


# Create a custom commit parser class
class CustomCommitParser(semantic_release.CommitParser[semantic_release.ParseResult, object]):
    """A custom commit parser class to parse commit messages."""

    def parse(self, commit: git.objects.commit.Commit) -> semantic_release.ParseResult:
        """Parse a given Git commit and determine its semantic version type.

        This method checks the commit message for specific patterns to classify the commit:
        - If the commit message starts with 'release', it is excluded.
        - If the commit message starts with 'Merge', it is classified as a merge commit.
        - If the commit message is a breaking change, it is classified as a breaking change.
        - For all other commits, it uses the Angular commit parser or returns 'Unknown' for unsupported types.

        Parameters
        ----------
        commit : object
            The Git commit object to be parsed.

        Returns
        -------
        result : object
            The parsed commit result.

        """

        # Get the commit message and strip any extra whitespace
        commit_message = commit.message.strip()

        # Exclude release-related commits (e.g., 'Release x.x.x')
        if commit_message.lower().startswith("release"):
            # Exclude other release-related commits
            return semantic_release.ParseError(commit=commit, error="Release commit excluded")

        # If the commit is a merge, assign type "Merges"
        if commit_message.lower().startswith("merge"):
            return semantic_release.ParsedCommit(
                bump=semantic_release.enums.LevelBump.NO_RELEASE,
                commit=commit,
                type="Merges",
                scope=None,
                descriptions=[commit_message],
                breaking_descriptions=[],
            )

        # Identify breaking changes (e.g., "feat!") for a major bump.
        # By default, "BREAKING CHANGE:" is used, but "feat!" and "fix!"
        # should also be considered with type "Breaking changes".
        if commit_message.split(":")[0].endswith("!"):
            return semantic_release.ParsedCommit(
                bump=semantic_release.enums.LevelBump.MAJOR,
                commit=commit,
                type="Breaking changes",
                scope=None,
                descriptions=[commit_message],
                breaking_descriptions=[],
            )

        # Use Angular parser for standard types
        # Source: https://python-semantic-release.readthedocs.io/en/latest/commit_parsing.html#angular-commit-parser
        angular_parser = semantic_release.commit_parser.AngularCommitParser()
        result = angular_parser.parse(commit)

        return result
