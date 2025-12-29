# Release Process

This document describes how to create a new release of vi-sudoku.

## Automated Release Process

The project uses GitHub Actions to automatically build binaries and create releases.

### Creating a New Release

1. **Update the version** in `pyproject.toml` if needed:
   ```toml
   version = "0.2.0"
   ```

2. **Commit and push** your changes:
   ```sh
   git add pyproject.toml
   git commit -m "Bump version to 0.2.0"
   git push origin main
   ```

3. **Create and push a version tag**:
   ```sh
   git tag v0.2.0
   git push origin v0.2.0
   ```

4. **Automated Build**: The GitHub Actions workflow will automatically:
   - Build binaries for:
     - Linux (x86_64)
     - macOS Intel (x86_64)
     - macOS Apple Silicon (ARM64)
     - Windows (x86_64)
   - Create a GitHub release with the tag
   - Attach all binaries to the release
   - Generate release notes automatically

5. **Review the release**: Visit the [Releases page](https://github.com/ndy7stillx86ihz/vi-sudoku/releases) to verify the release was created successfully.

## Manual Testing Before Release

Before pushing a tag, test the build locally:

### Linux/macOS:
```sh
./build.sh
./dist/vi-sudoku
```

### Windows:
```cmd
build.bat
dist\vi-sudoku.exe
```

## Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Test the build locally
- [ ] Commit version changes
- [ ] Create and push version tag
- [ ] Verify GitHub Actions workflow completes successfully
- [ ] Test downloaded binaries on each platform
- [ ] Update release notes if needed

## Troubleshooting

### Build fails on GitHub Actions
- Check the workflow logs in the "Actions" tab
- Ensure the `.spec` file includes all necessary dependencies
- Test the build locally first

### Binary doesn't run
- Check that all Python dependencies are included in the spec file
- Verify the target platform matches the build platform
- Test with `--debug` flag: `pyinstaller vi-sudoku.spec --debug`

## Pre-releases

To create a pre-release (e.g., beta, rc):

```sh
git tag v0.2.0-beta.1
git push origin v0.2.0-beta.1
```

Mark the release as a pre-release in the GitHub UI after it's created.
